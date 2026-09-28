from app.services.chunking.text_chunker import TextChunker
from app.services.vector.chroma_store import ChromaStore


class ResearchIndexer:

    def __init__(self):

        self.chunker = TextChunker(
            chunk_size=1000,
            chunk_overlap=200,
        )

        self.vector_store = ChromaStore()

    def index_source(
        self,
        source_id: int,
        project_id: int,
        title: str,
        url: str,
        content: str,
    ):

        chunks = self.chunker.split(content)

        if not chunks:
            return 0

        documents = []
        metadatas = []
        ids = []

        for chunk in chunks:

            documents.append(chunk.text)

            metadatas.append(
                {
                    "source_id": str(source_id),
                    "project_id": str(project_id),
                    "title": title,
                    "url": url,
                    "chunk_index": chunk.chunk_index,
                }
            )

            ids.append(
                f"source-{source_id}-chunk-{chunk.chunk_index}"
            )

        self.vector_store.add_chunks(
            chunks=documents,
            metadatas=metadatas,
            ids=ids,
        )

        return len(chunks)