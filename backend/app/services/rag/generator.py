from app.services.llm.ollama_client import OllamaClient
from app.services.rag.retriever import ResearchRetriever


class RAGGenerator:

    def __init__(self):

        self.retriever = ResearchRetriever()
        self.llm = OllamaClient()

    async def generate(
        self,
        question: str,
        n_results: int = 5,
    ):

        chunks = self.retriever.retrieve(
            query=question,
            n_results=n_results,
        )

        if not chunks:
            return {
                "answer": "No relevant research sources were found.",
                "sources": [],
            }

        context_parts = []

        for index, chunk in enumerate(
            chunks,
            start=1,
        ):

            context_parts.append(
                f"""
SOURCE {index}

Title:
{chunk["title"]}

URL:
{chunk["url"]}

Content:
{chunk["text"]}
"""
            )

        context = "\n".join(context_parts)

        prompt = f"""
You are an AI research assistant.

Answer the user's research question using ONLY
the research sources provided below.

If the sources do not contain enough information,
say that the available sources are insufficient.

Do not invent facts.

Cite sources using [Source 1], [Source 2], etc.

Research Question:
{question}

Research Sources:
{context}

Instructions:

1. Give a clear and structured answer.
2. Use information from the provided sources.
3. Do not invent information.
4. Include citations in the form [Source X].
5. If sources disagree, mention the disagreement.
6. Separate established information from uncertainty.
"""

        answer = await self.llm.generate(prompt)

        return {
            "answer": answer,
            "sources": chunks,
        }