from app.rag.vector_store import VectorStore
from app.rag.ranker import rank_chunks


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

    ranked = rank_chunks(results, question)

    for i, result in enumerate(ranked[:5]):

        metadata = result["metadata"]

        print("\nResult:", i + 1)

        print(
            "File:",
            metadata["filename"]
        )

        print(
            "Heading:",
            metadata["heading"]
        )

        print(
            "Status:",
            metadata.get("status")
        )

        print(
            "Distance:",
            result["distance"]
        )

        print(
            "Final score:",
            result["score"]
        )

        print(
            "Text:",
            result["text"][:300]
        )
