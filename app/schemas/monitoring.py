from typing import List
from pydantic import BaseModel


class QueryLogEntry(BaseModel):
    request_id: str
    query: str
    cache_hit: bool
    used_reranker: bool
    retrieval_count: int
    retrieval_ms: float
    rerank_ms: float
    generation_ms: float
    total_ms: float


class MonitoringStatsResponse(BaseModel):
    total_queries: int
    cache_hit_rate: float
    avg_retrieval_count: float
    avg_retrieval_ms: float
    avg_rerank_ms: float
    avg_generation_ms: float
    avg_total_ms: float


class MonitoringLogsResponse(BaseModel):
    total_logs: int
    logs: List[QueryLogEntry]