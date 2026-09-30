import pytest

from app.services.llm.ollama_client import OllamaClient


@pytest.mark.asyncio
async def test_ollama_generation():

    client = OllamaClient()

    response = await client.generate(
        "Explain RAG in two sentences."
    )

    assert response
    assert len(response) > 10

    print("\nLLM RESPONSE:")
    print(response)