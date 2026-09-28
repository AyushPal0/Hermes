from dataclasses import dataclass


@dataclass
class TextChunk:
    text: str
    chunk_index: int


class TextChunker:

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> list[TextChunk]:

        if not text.strip():
            return []

        text = " ".join(text.split())

        chunks = []

        start = 0
        chunk_index = 0

        while start < len(text):

            end = start + self.chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    TextChunk(
                        text=chunk_text,
                        chunk_index=chunk_index,
                    )
                )

                chunk_index += 1

            start = end - self.chunk_overlap

        return chunks