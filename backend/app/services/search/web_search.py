from app.services.search.base import SearchResult
from app.services.search.ddgs_search import DDGSSearchProvider


class WebSearchService:

    def __init__(self):
        self.provider = DDGSSearchProvider()

    async def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[SearchResult]:

        return await self.provider.search(
            query=query,
            max_results=max_results,
        )