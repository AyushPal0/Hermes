from ddgs import DDGS

from app.services.search.base import SearchResult


class DDGSSearchProvider:

    async def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[SearchResult]:

        results = DDGS().text(
            query,
            max_results=max_results,
        )

        search_results = []

        for result in results:
            search_results.append(
                SearchResult(
                    title=result.get("title", ""),
                    url=result.get("href", ""),
                    snippet=result.get("body", ""),
                )
            )

        return search_results