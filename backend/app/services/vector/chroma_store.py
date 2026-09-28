import chromadb


class ChromaStore:

    def __init__(
        self,
        persist_directory: str = "chroma_db",
    ):

        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = self.client.get_or_create_collection(
            name="research_chunks"
        )

    def add_chunks(
        self,
        chunks: list[str],
        metadatas: list[dict],
        ids: list[str],
    ):

        self.collection.add(
            documents=chunks,
            metadatas=metadatas,
            ids=ids,
        )

    def search(
        self,
        query: str,
        n_results: int = 5,
    ):

        return self.collection.query(
            query_texts=[query],
            n_results=n_results,
        )