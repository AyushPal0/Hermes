from app.services.chunking.text_chunker import TextChunker


def test_text_chunking():

    text = "A" * 2500

    chunker = TextChunker(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = chunker.split(text)

    assert len(chunks) > 1

    assert chunks[0].chunk_index == 0

    assert chunks[1].chunk_index == 1