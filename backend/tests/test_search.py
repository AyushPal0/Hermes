import pytest

from app.services.search.web_search import WebSearchService


@pytest.mark.asyncio
async def test_web_search():

    service = WebSearchService()

    results = await service.search(
        "artificial intelligence",
        max_results=3,
    )

    assert len(results) > 0

    for result in results:
        print(result)

        assert result.title
        assert result.url