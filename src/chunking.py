from typing import Iterable

def chunk_text(text: str, source_id: str, chunk_size: int = 55, overlap: int = 10) -> list[dict]:
    """Split text into overlapping word chunks while retaining source identifiers."""
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Require chunk_size > overlap >= 0.")

    words = text.split()
    chunks = []
    step = chunk_size - overlap

    for start in range(0, len(words), step):
        part = words[start:start + chunk_size]
        if not part:
            break
        chunks.append({
            "source_id": source_id,
            "chunk_id": f"{source_id}-{len(chunks) + 1}",
            "text": " ".join(part),
        })
        if start + chunk_size >= len(words):
            break

    return chunks


def chunk_documents(documents: Iterable[dict], chunk_size: int = 55, overlap: int = 10) -> list[dict]:
    chunks = []
    for document in documents:
        chunks.extend(chunk_text(document["text"], document["id"], chunk_size, overlap))
    return chunks
