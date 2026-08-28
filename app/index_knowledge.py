from app.rag.loader import load_markdown_documents
from app.rag.chunker import chunk_document
from app.rag.vector_store import VectorStore


def main():
    print("Loading documents...")

    documents = load_markdown_documents(
        "knowledge-base"
    )

    chunks = []

    for document in documents:
        chunks.extend(
            chunk_document(document)
        )

    print(f"Loaded {len(documents)} documents")
    print(f"Created {len(chunks)} chunks")

    print("Creating vector database...")

    vector_store = VectorStore()

    vector_store.add_chunks(chunks)

    print("Knowledge base indexed successfully!")


if __name__ == "__main__":
    main()
