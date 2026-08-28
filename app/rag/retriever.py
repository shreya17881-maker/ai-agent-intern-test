from app.rag.vector_store import VectorStore
from app.rag.ranker import rank_chunks


class Retriever:
    """
    Retrieves and re-ranks relevant knowledge chunks.
    """

    def __init__(self):
        self.vector_store = VectorStore()

    def retrieve(self, question, n_results=10, top_k=5):
        """
        Retrieve relevant chunks for a question
        and return the top-ranked chunks.
        """

        results = self.vector_store.search(
            question,
            n_results=n_results
        )

        ranked = rank_chunks(
            results,
            question
        )

        return ranked[:top_k]
