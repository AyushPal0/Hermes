import asyncio

from sqlalchemy.orm import Session

from app.models.research_project import ResearchProject
from app.models.research_source import ResearchSource
from app.services.extraction.webpage import extract_webpage
from app.services.search.web_search import WebSearchService


class ResearchPipeline:

    def __init__(self, db: Session):

        self.db = db
        self.search_service = WebSearchService()

    async def run(
        self,
        project: ResearchProject,
        max_results: int = 5,
    ):

        search_results = await self.search_service.search(
            project.question,
            max_results=max_results,
        )

        semaphore = asyncio.Semaphore(3)

        async def process_result(result):

            async with semaphore:

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

                return result, extracted

        tasks = [
            process_result(result)
            for result in search_results
        ]

        processed_results = await asyncio.gather(
            *tasks
        )

        sources = []

        for result, extracted in processed_results:

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

            sources.append(source)

        self.db.commit()

        for source in sources:
            self.db.refresh(source)

        return sources