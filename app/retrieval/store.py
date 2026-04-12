from typing import Dict, List


class InMemoryDocumentStore:
    """
    Temporary in-memory store for chunks.
    """

    def __init__(self) -> None:
        self._chunks: List[Dict] = []

    def add_chunks(self, chunks: List[Dict]) -> None:
        self._chunks.extend(chunks)

    def get_all_chunks(self) -> List[Dict]:
        return self._chunks

    def clear(self) -> None:
        self._chunks = []

    def count(self) -> int:
        return len(self._chunks)


document_store = InMemoryDocumentStore()