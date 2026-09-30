import asyncio

from sqlalchemy.orm import Session

from app.models.research_project import ResearchProject
from app.models.research_source import ResearchSource

from app.services.agent.planner import ResearchPlanner
from app.services.extraction.webpage import extract_webpage
from app.services.search.web_search import WebSearchService
from app.services.indexing.research_indexer import ResearchIndexer


class ResearchAgent:

    def __init__(self, db: Session):

        self.db = db

        self.planner = ResearchPlanner()
        self.search_service = WebSearchService()
        self.indexer = ResearchIndexer()

    async def run(
        self,
        project: ResearchProject,
    ):

        # -----------------------------------------
        # STEP 1: CREATE RESEARCH PLAN
        # -----------------------------------------

        plan = await self.planner.create_plan(
            question=project.question,
            depth=project.depth,
        )

        # -----------------------------------------
        # STEP 2: SEARCH EACH SUB-QUESTION
        # -----------------------------------------

        all_results = []

        for sub_question in plan:

            results = await self.search_service.search(
                query=sub_question,
                max_results=3,
            )

            for result in results:

                all_results.append(
                    {
                        "sub_question": sub_question,
                        "result": result,
                    }
                )

        # -----------------------------------------
        # STEP 3: REMOVE DUPLICATE URLs
        # -----------------------------------------

        unique_results = {}

        for item in all_results:

            result = item["result"]

            if result.url not in unique_results:

                unique_results[result.url] = item

        research_results = list(
            unique_results.values()
        )

        # -----------------------------------------
        # STEP 4: EXTRACT WEBPAGES
        # -----------------------------------------

        semaphore = asyncio.Semaphore(3)

        async def process_result(item):

            async with semaphore:

                result = item["result"]

                try:

                    extracted = await extract_webpage(
                        result.url
                    )

                except Exception:

                    extracted = {
                        "url": result.url,
                        "title": result.title,
                        "author": "",
                        "date": "",
                        "text": "",
                    }

                return item, extracted

        tasks = [
            process_result(item)
            for item in research_results
        ]

        processed = await asyncio.gather(
            *tasks
        )

        # -----------------------------------------
        # STEP 5: SAVE SOURCES
        # -----------------------------------------

        sources = []

        for item, extracted in processed:

            result = item["result"]
            sub_question = item["sub_question"]

            source = ResearchSource(
                project_id=project.id,
                title=(
                    extracted["title"]
                    or result.title
                ),
                url=result.url,
                snippet=result.snippet,
                content=extracted["text"][:100000],
                author=extracted["author"],
                published_at=extracted["date"],
            )

            self.db.add(source)

            sources.append(
                {
                    "source": source,
                    "sub_question": sub_question,
                }
            )

        self.db.commit()

        # -----------------------------------------
        # STEP 6: INDEX SOURCES
        # -----------------------------------------

        indexed_chunks = 0

        for item in sources:

            source = item["source"]

            self.db.refresh(source)

            chunk_count = self.indexer.index_source(
                source_id=source.id,
                project_id=source.project_id,
                title=source.title,
                url=source.url,
                content=source.content,
            )

            indexed_chunks += chunk_count

        return {
            "plan": plan,
            "source_count": len(sources),
            "indexed_chunks": indexed_chunks,
            "sources": [
                item["source"]
                for item in sources
            ],
        }