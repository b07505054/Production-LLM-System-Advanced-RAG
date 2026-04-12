from typing import Dict, List


class InMemoryVectorStore:
    """
    Temporary in-memory vector store.

    Each item contains:
    - chunk metadata
    - text
    - embedding vector
    """

    def __init__(self) -> None:
        self._items: List[Dict] = []

    def add_items(self, items: List[Dict]) -> None:
        self._items.extend(items)

    def get_all_items(self) -> List[Dict]:
        return self._items

    def clear(self) -> None:
        self._items = []

    def count(self) -> int:
        return len(self._items)


vector_store = InMemoryVectorStore()