from typing import List
from pydantic import BaseModel, Field


class RetrievalEvalExample(BaseModel):
    query: str = Field(..., min_length=1)
    gold_chunk_ids: List[str] = Field(..., min_length=1)
    top_k: int = Field(default=3, ge=1, le=20)


class RetrievalEvalResult(BaseModel):
    query: str
    gold_chunk_ids: List[str]
    retrieved_chunk_ids: List[str]
    hit_at_k: int
    recall_at_k: float
    reciprocal_rank: float


class RetrievalEvalSummary(BaseModel):
    num_examples: int
    avg_hit_at_k: float
    avg_recall_at_k: float
    mrr: float
    results: List[RetrievalEvalResult]


class RetrievalComparisonSummary(BaseModel):
    retrieval_only: RetrievalEvalSummary
    retrieval_with_rerank: RetrievalEvalSummary