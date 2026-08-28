from pathlib import Path
import yaml


def load_markdown_documents(directory):
    """
    Load all Markdown files from the knowledge-base directory.

    Returns a list of documents containing:
    - file name
    - metadata
    - document content
    """

    documents = []

    directory = Path(directory)

    for file_path in directory.glob("*.md"):
        text = file_path.read_text(encoding="utf-8")

        # Check whether the file contains YAML front matter
        if text.startswith("---"):
            parts = text.split("---", 2)

            metadata_text = parts[1]
            content = parts[2].strip()

            metadata = yaml.safe_load(metadata_text) or {}
        else:
            metadata = {}
            content = text.strip()

        metadata["filename"] = file_path.name

        documents.append(
            {
                "content": content,
                "metadata": metadata,
            }
        )

    return documents
