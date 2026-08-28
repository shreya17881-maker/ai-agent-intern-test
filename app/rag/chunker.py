import re


def chunk_document(document):
    """
    Split a Markdown document into useful sections.

    Top-level document titles (# Title) are kept as context
    but are not stored as standalone chunks.
    """

    content = document["content"]
    base_metadata = document["metadata"]

    # Find all ## headings and the content following them.
    matches = list(
        re.finditer(r"(?m)^##\s+(.+)$", content)
    )

    chunks = []

    for i, match in enumerate(matches):

        heading = match.group(1).strip()

        start = match.start()
        end = (
            matches[i + 1].start()
            if i + 1 < len(matches)
            else len(content)
        )

        section = content[start:end].strip()

        # Ignore extremely small sections
        if len(section) < 30:
            continue

        metadata = base_metadata.copy()
        metadata["heading"] = heading

        chunks.append(
            {
                "text": section,
                "metadata": metadata,
            }
        )

    return chunks
