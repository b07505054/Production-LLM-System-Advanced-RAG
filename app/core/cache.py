from typing import Any, Dict, Optional


class SimpleQueryCache:
    """
    Very simple in-memory cache for query responses.

    Key:
    - normalized query signature

    Value:
    - response payload
    """

    def __init__(self) -> None:
        self._store: Dict[str, Dict[str, Any]] = {}

    def make_key(self, query: str, top_k: int, use_reranker: bool) -> str:
        normalized_query = query.strip().lower()
        return f"{normalized_query}::top_k={top_k}::reranker={use_reranker}"

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        return self._store.get(key)

    def set(self, key: str, value: Dict[str, Any]) -> None:
        self._store[key] = value

    def clear(self) -> int:
        count = len(self._store)
        self._store = {}
        return count

    def count(self) -> int:
        return len(self._store)


query_cache = SimpleQueryCache()