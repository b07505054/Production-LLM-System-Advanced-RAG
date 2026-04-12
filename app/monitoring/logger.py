from typing import List

from app.schemas.monitoring import QueryLogEntry


class QueryMonitoringStore:
    """
    Simple in-memory monitoring store for query logs.
    """

    def __init__(self) -> None:
        self._logs: List[QueryLogEntry] = []

    def add_log(self, entry: QueryLogEntry) -> None:
        self._logs.append(entry)

    def get_logs(self, limit: int = 20) -> List[QueryLogEntry]:
        return self._logs[-limit:][::-1]

    def count(self) -> int:
        return len(self._logs)

    def clear(self) -> int:
        count = len(self._logs)
        self._logs = []
        return count

    def get_all_logs(self) -> List[QueryLogEntry]:
        return self._logs


query_monitoring_store = QueryMonitoringStore()