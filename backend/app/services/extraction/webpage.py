import asyncio

import trafilatura


async def extract_webpage(url: str) -> dict:

    html = await asyncio.to_thread(
        trafilatura.fetch_url,
        url,
    )

    if not html:
        return {
            "url": url,
            "title": "",
            "author": "",
            "date": "",
            "text": "",
        }

    document = await asyncio.to_thread(
        trafilatura.bare_extraction,
        html,
        url=url,
    )

    if not document:
        return {
            "url": url,
            "title": "",
            "author": "",
            "date": "",
            "text": "",
        }

    data = document.as_dict()

    return {
        "url": data.get("url") or url,
        "title": data.get("title") or "",
        "author": data.get("author") or "",
        "date": data.get("date") or "",
        "text": data.get("text") or "",
    }