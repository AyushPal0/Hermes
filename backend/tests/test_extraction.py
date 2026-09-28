import pytest

from app.services.extraction.webpage import extract_webpage


@pytest.mark.asyncio
async def test_webpage_extraction():

    url = "https://en.wikipedia.org/wiki/Artificial_intelligence"

    result = await extract_webpage(url)

    assert result["url"]
    assert result["text"]

    print("\nTITLE:")
    print(result["title"])

    print("\nTEXT PREVIEW:")
    print(result["text"][:500])