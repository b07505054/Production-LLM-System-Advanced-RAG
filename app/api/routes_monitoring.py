from fastapi import APIRouter, Query

from app.monitoring.logger import query_monitoring_store
from app.schemas.monitoring import (
    MonitoringLogsResponse,
    MonitoringStatsResponse,
)


router = APIRouter(prefix="/monitoring", tags=["monitoring"])


@router.get("/logs", response_model=MonitoringLogsResponse)
def get_monitoring_logs(limit: int = Query(default=10, ge=1, le=100)) -> MonitoringLogsResponse:
    logs = query_monitoring_store.get_logs(limit=limit)
    return MonitoringLogsResponse(
        total_logs=query_monitoring_store.count(),
        logs=logs,
    )


@router.get("/stats", response_model=MonitoringStatsResponse)
def get_monitoring_stats() -> MonitoringStatsResponse:
    logs = query_monitoring_store.get_all_logs()

    if not logs:
        return MonitoringStatsResponse(
            total_queries=0,
            cache_hit_rate=0.0,
            avg_retrieval_count=0.0,
            avg_retrieval_ms=0.0,
            avg_rerank_ms=0.0,
            avg_generation_ms=0.0,
            avg_total_ms=0.0,
        )

    total_queries = len(logs)
    cache_hits = sum(1 for log in logs if log.cache_hit)

    return MonitoringStatsResponse(
        total_queries=total_queries,
        cache_hit_rate=round(cache_hits / total_queries, 4),
        avg_retrieval_count=round(sum(log.retrieval_count for log in logs) / total_queries, 4),
        avg_retrieval_ms=round(sum(log.retrieval_ms for log in logs) / total_queries, 4),
        avg_rerank_ms=round(sum(log.rerank_ms for log in logs) / total_queries, 4),
        avg_generation_ms=round(sum(log.generation_ms for log in logs) / total_queries, 4),
        avg_total_ms=round(sum(log.total_ms for log in logs) / total_queries, 4),
    )