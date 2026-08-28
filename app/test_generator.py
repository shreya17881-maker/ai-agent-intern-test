from app.rag.vector_store import VectorStore
from app.rag.ranker import rank_chunks
from app.rag.generator import generate_answer


vector_store = VectorStore()


questions = [
    "How many days do I have to return an item?",
    "Do you ship to Canada?",
    "Can I cancel my order?",
]


for question in questions:

    print("\n================================")
    print("QUESTION:", question)
    print("================================")

    results = vector_store.search(
        question,
        n_results=10
    )

    ranked = rank_chunks(
        results,
        question
    )

    top_chunks = ranked[:5]

    print("\n--- CONTEXT SENT TO LLM ---")

    for chunk in top_chunks:
        print("\nFILE:", chunk["metadata"]["filename"])
        print("HEADING:", chunk["metadata"]["heading"])
        print("TEXT:", chunk["text"])

    print("\n--- END CONTEXT ---")

    answer = generate_answer(
        question,
        top_chunks
    )

    print("\nANSWER:")
    print(answer)
