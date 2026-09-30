from app.services.vector.chroma_store import ChromaStore


class ResearchRetriever:

    def __init__(self):

        self.vector_store = ChromaStore()

    def retrieve(
        self,
        query: str,
        n_results: int = 5,
    ):

        results = self.vector_store.search(
            query=query,
            n_results=n_results,
        )

        documents = results.get(
            "documents",
            [[]],
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]],
        )[0]

        retrieved_chunks = []

        for document, metadata in zip(
            documents,
            metadatas,
        ):

            retrieved_chunks.append(
                {
                    "text": document,
                    "source_id": metadata.get(
                        "source_id"
                    ),
                    "title": metadata.get(
                        "title"
                    ),
                    "url": metadata.get(
                        "url"
                    ),
                    "chunk_index": metadata.get(
                        "chunk_index"
                    ),
                }
            )

        return retrieved_chunks