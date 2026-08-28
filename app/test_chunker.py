from app.rag.loader import load_markdown_documents
from app.rag.chunker import chunk_document


documents = load_markdown_documents("knowledge-base")

chunks = []

for document in documents:
    document_chunks = chunk_document(document)
    chunks.extend(document_chunks)


print("Documents:", len(documents))
print("Chunks:", len(chunks))

print("\nFirst 5 chunks:\n")

for chunk in chunks[:5]:
    print("--------------------------------")
    print("FILE:", chunk["metadata"]["filename"])
    print("HEADING:", chunk["metadata"]["heading"])
    print("STATUS:", chunk["metadata"].get("status"))
    print("TEXT:")
    print(chunk["text"][:300])
