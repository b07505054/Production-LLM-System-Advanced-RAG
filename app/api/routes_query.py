import time
import uuid

from fastapi import APIRouter, HTTPException
from app.generation.answer_generator import answer_generator
from app.schemas.query import (
    QueryRequest,
    QueryResponse,
    ChunkResult,
    QueryMetrics,
    LatencyBreakdown,
)
from app.retrieval.vector_store import vector_store
from app.retrieval.retriever import retrieve_chunks
from app.retrieval.reranker import simple_rerank
from app.core.cache import query_cache
from app.monitoring.logger import query_monitoring_store
from app.schemas.monitoring import QueryLogEntry


router = APIRouter(prefix="/query", tags=["query"])


@router.post("", response_model=QueryResponse)
def query_documents(payload: QueryRequest) -> QueryResponse:
    request_id = f"req_{uuid.uuid4().hex[:12]}"
    total_start = time.perf_counter()

    try:
        all_items = vector_store.get_all_items()

        if not all_items:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "EMPTY_STORE",
                    "message": "No documents have been ingested yet.",
                    "request_id": request_id,
                },
            )

        cache_key = query_cache.make_key(
            query=payload.query,
            top_k=payload.top_k,
            use_reranker=payload.use_reranker,
        )
        cached_response = query_cache.get(cache_key)

        if cached_response is not None:
            total_ms = round((time.perf_counter() - total_start) * 1000, 2)

            query_monitoring_store.add_log(
                QueryLogEntry(
                    request_id=request_id,
                    query=payload.query,
                    cache_hit=True,
                    used_reranker=payload.use_reranker,
                    retrieval_count=len(cached_response["retrieved_chunks"]),
                    retrieval_ms=0.0,
                    rerank_ms=0.0,
                    generation_ms=0.0,
                    total_ms=total_ms,
                )
            )

            return QueryResponse(
                request_id=request_id,
                answer=cached_response["answer"],
                citations=cached_response["citations"],
                retrieved_chunks=cached_response["retrieved_chunks"] if payload.debug else [],
                reranked_chunks=cached_response["reranked_chunks"] if (payload.debug and payload.use_reranker) else None,
                latency_ms=total_ms,
                used_reranker=payload.use_reranker,
                metrics=QueryMetrics(
                    retrieval_count=len(cached_response["retrieved_chunks"]),
                    used_reranker=payload.use_reranker,
                    cache_hit=True,
                ),
                latency_breakdown=LatencyBreakdown(
                    retrieval_ms=0.0,
                    rerank_ms=0.0,
                    generation_ms=0.0,
                    total_ms=total_ms,
                ),
            )

        retrieval_start = time.perf_counter()
        retrieved_raw = retrieve_chunks(
            query=payload.query,
            items=all_items,
            top_k=payload.top_k,
        )
        retrieval_ms = round((time.perf_counter() - retrieval_start) * 1000, 2)

        if not retrieved_raw:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "NO_RELEVANT_CHUNKS",
                    "message": "No relevant chunks found for the query.",
                    "request_id": request_id,
                },
            )

        retrieved_chunks = [
            ChunkResult(
                chunk_id=item["chunk_id"],
                doc_id=item["doc_id"],
                text=item["text"],
                score=item["score"],
            )
            for item in retrieved_raw
        ]

        reranked_chunks = None
        final_chunks = retrieved_chunks
        rerank_ms = 0.0

        if payload.use_reranker:
            rerank_start = time.perf_counter()
            reranked_chunks = simple_rerank(retrieved_chunks, payload.query)
            rerank_ms = round((time.perf_counter() - rerank_start) * 1000, 2)
            final_chunks = reranked_chunks

        generation_start = time.perf_counter()
        answer = answer_generator.generate(payload.query, final_chunks)
        generation_ms = round((time.perf_counter() - generation_start) * 1000, 2)
        total_ms = round((time.perf_counter() - total_start) * 1000, 2)

        query_cache.set(
            cache_key,
            {
                "answer": answer,
                "citations": final_chunks[:3],
                "retrieved_chunks": retrieved_chunks,
                "reranked_chunks": reranked_chunks,
            },
        )

        query_monitoring_store.add_log(
            QueryLogEntry(
                request_id=request_id,
                query=payload.query,
                cache_hit=False,
                used_reranker=payload.use_reranker,
                retrieval_count=len(retrieved_chunks),
                retrieval_ms=retrieval_ms,
                rerank_ms=rerank_ms,
                generation_ms=generation_ms,
                total_ms=total_ms,
            )
        )

        return QueryResponse(
            request_id=request_id,
            answer=answer,
            citations=final_chunks[:3],
            retrieved_chunks=retrieved_chunks if payload.debug else [],
            reranked_chunks=reranked_chunks if (payload.debug and payload.use_reranker) else None,
            latency_ms=total_ms,
            used_reranker=payload.use_reranker,
            metrics=QueryMetrics(
                retrieval_count=len(retrieved_chunks),
                used_reranker=payload.use_reranker,
                cache_hit=False,
            ),
            latency_breakdown=LatencyBreakdown(
                retrieval_ms=retrieval_ms,
                rerank_ms=rerank_ms,
                generation_ms=generation_ms,
                total_ms=total_ms,
            ),
        )

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "QUERY_PIPELINE_ERROR",
                "message": str(exc),
                "request_id": request_id,
            },
        ) from exc