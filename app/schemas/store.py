from pydantic import BaseModel


class StoreStatsResponse(BaseModel):
    num_vector_items: int
    cache_size: int


class ClearStoreResponse(BaseModel):
    message: str
    cleared_vector_items: int
    cleared_cache_entries: int