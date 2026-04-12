from typing import List, Dict


def chunk_text(
    doc_id: str,
    title: str,
    text: str,
    chunk_size: int = 300,
    chunk_overlap: int = 50,
) -> List[Dict]:
    text = text.strip()
    if not text:
        return []

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks = []
    start = 0
    chunk_index = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk_text_value = text[start:end].strip()

        if chunk_text_value:
            chunks.append(
                {
                    "chunk_id": f"{doc_id}_chunk_{chunk_index:03d}",
                    "doc_id": doc_id,
                    "title": title,
                    "chunk_index": chunk_index,
                    "text": chunk_text_value,
                }
            )

        if end == len(text):
            break

        start += chunk_size - chunk_overlap
        chunk_index += 1

    return chunks