import chromadb
from sentence_transformers import SentenceTransformer


def clean_metadata(metadata):
    """
    Convert metadata values into types supported by ChromaDB.
    """

    cleaned = {}

    for key, value in metadata.items():
        if value is None:
            continue

        # Convert dates and other non-supported objects to strings
        if isinstance(value, (str, int, float, bool)):
            cleaned[key] = value
        else:
            cleaned[key] = str(value)

    return cleaned


class VectorStore:
    def __init__(self, collection_name="knowledge_base"):
        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def add_chunks(self, chunks):

        documents = [
            chunk["text"]
            for chunk in chunks
        ]

        metadatas = [
            clean_metadata(chunk["metadata"])
            for chunk in chunks
        ]

        ids = [
            f"chunk-{i}"
            for i in range(len(chunks))
        ]

        embeddings = self.embedding_model.encode(
            documents
        ).tolist()

        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings
        )

    def search(self, query, n_results=5):

        query_embedding = self.embedding_model.encode(
            [query]
        ).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )

        return results
