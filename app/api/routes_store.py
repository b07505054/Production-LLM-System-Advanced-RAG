from fastapi import APIRouter

from app.retrieval.vector_store import vector_store
from app.core.cache import query_cache
from app.schemas.store import StoreStatsResponse, ClearStoreResponse


router = APIRouter(prefix="/store", tags=["store"])


@router.get("/stats", response_model=StoreStatsResponse)
def get_store_stats() -> StoreStatsResponse:
    return StoreStatsResponse(
        num_vector_items=vector_store.count(),
        cache_size=query_cache.count(),
    )


@router.post("/clear", response_model=ClearStoreResponse)
def clear_store() -> ClearStoreResponse:
    cleared_vector_items = vector_store.count()
    vector_store.clear()

    cleared_cache_entries = query_cache.clear()

    return ClearStoreResponse(
        message="Vector store and query cache cleared successfully",
        cleared_vector_items=cleared_vector_items,
        cleared_cache_entries=cleared_cache_entries,
    )