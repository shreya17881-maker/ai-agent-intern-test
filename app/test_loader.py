from app.rag.loader import load_markdown_documents


documents = load_markdown_documents("knowledge-base")

print("Documents loaded:", len(documents))

for document in documents[:2]:
    print("\nFILE:", document["metadata"]["filename"])
    print("TITLE:", document["metadata"].get("title"))
    print("STATUS:", document["metadata"].get("status"))
