from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from pydantic import BaseModel


class QueryMetrics(BaseModel):
    retrieval_count: int
    used_reranker: bool
    cache_hit: bool

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="User query text")
    top_k: int = Field(default=5, ge=1, le=50)
    use_reranker: bool = Field(default=False)
    debug: bool = Field(default=False)

    @field_validator("query")
    @classmethod
    def validate_query(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("query must not be empty")
        return value


class ChunkResult(BaseModel):
    chunk_id: str
    doc_id: str
    text: str
    score: float


class ErrorInfo(BaseModel):
    code: str
    message: str
    request_id: str

class LatencyBreakdown(BaseModel):
    retrieval_ms: float
    rerank_ms: float
    generation_ms: float
    total_ms: float
class QueryResponse(BaseModel):
    request_id: str
    answer: str
    citations: List[ChunkResult] = Field(default_factory=list)
    retrieved_chunks: List[ChunkResult] = Field(default_factory=list)
    reranked_chunks: Optional[List[ChunkResult]] = None
    latency_ms: float
    used_reranker: bool
    metrics: QueryMetrics
    latency_breakdown: LatencyBreakdown


class ErrorResponse(BaseModel):
    error: ErrorInfo

