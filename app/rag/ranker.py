import re


STATUS_SCORE = {
    "active": 3,
    "superseded": -2,
    "draft": -3,
}


AUTHORITY_SCORE = {
    "official": 2,
}


AUDIENCE_SCORE = {
    "customer": 1,
    "internal": -1,
}


def get_keywords(question):
    """
    Extract useful keywords from the user's question.
    """

    stop_words = {
        "the",
        "a",
        "an",
        "is",
        "are",
        "do",
        "does",
        "can",
        "i",
        "to",
        "of",
        "for",
        "and",
        "or",
        "my",
        "have",
        "you",
        "how",
        "many",
        "what",
        "when",
        "where",
        "am",
    }

    words = re.findall(
        r"\b[a-zA-Z]+\b",
        question.lower()
    )

    return [
        word
        for word in words
        if word not in stop_words
        and len(word) > 2
    ]


def keyword_score(question, document):
    """
    Give extra points when the document directly
    answers the intent of the question.
    """

    question_lower = question.lower()
    document_lower = document.lower()

    score = 0

    # Return-window questions
    if (
        "return" in question_lower
        and (
            "how many days" in question_lower
            or "return window" in question_lower
        )
    ):
        if "day" in document_lower:
            score += 5

        if "return window" in document_lower:
            score += 5

        if "calendar days" in document_lower:
            score += 3

    # Shipping destination questions
    if (
        "ship" in question_lower
        and "canada" in question_lower
    ):
        if "canada" in document_lower:
            score += 5

        if "ships internationally" in document_lower:
            score += 5

    # Cancellation questions
    if "cancel" in question_lower:
        if "cancellation" in document_lower:
            score += 5

        if "cancel" in document_lower:
            score += 3

        if "30 minutes" in document_lower:
            score += 3

    # Generic keyword matching
    keywords = get_keywords(question)

    for keyword in keywords:
        if keyword in document_lower:
            score += 1

    return score

def rank_chunks(results, question):
    """
    Re-rank retrieved chunks using:

    1. Semantic similarity
    2. Keyword relevance
    3. Document status
    4. Policy authority
    5. Audience
    """

    ranked = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        status = metadata.get(
            "status",
            ""
        )

        authority = metadata.get(
            "policy_authority",
            ""
        )

        audience = metadata.get(
            "audience",
            ""
        )

        # Semantic relevance
        semantic_score = max(
            0,
            3 - distance
        )

        # Keyword relevance
        keyword_relevance = keyword_score(
            question,
            document
        )

        # Metadata scores
        status_score = STATUS_SCORE.get(
            status,
            0
        )

        authority_score = AUTHORITY_SCORE.get(
            authority,
            0
        )

        audience_score = AUDIENCE_SCORE.get(
            audience,
            0
        )

        # Final score
        score = (
            semantic_score
            + keyword_relevance
            + status_score
            + authority_score
            + audience_score
        )

        ranked.append(
            {
                "text": document,
                "metadata": metadata,
                "distance": distance,
                "score": score,
            }
        )

    ranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked
