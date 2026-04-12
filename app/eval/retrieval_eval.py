from typing import List, Set

from app.retrieval.retriever import retrieve_chunks
from app.retrieval.reranker import simple_rerank
from app.retrieval.vector_store import vector_store
from app.schemas.eval import (
    RetrievalEvalExample,
    RetrievalEvalResult,
    RetrievalEvalSummary,
    RetrievalComparisonSummary,
)
from app.schemas.query import ChunkResult


def compute_hit_at_k(retrieved_ids: List[str], gold_ids: Set[str]) -> int:
    return int(any(chunk_id in gold_ids for chunk_id in retrieved_ids))


def compute_recall_at_k(retrieved_ids: List[str], gold_ids: Set[str]) -> float:
    if not gold_ids:
        return 0.0

    hits = sum(1 for chunk_id in retrieved_ids if chunk_id in gold_ids)
    return hits / len(gold_ids)


def compute_reciprocal_rank(retrieved_ids: List[str], gold_ids: Set[str]) -> float:
    for rank, chunk_id in enumerate(retrieved_ids, start=1):
        if chunk_id in gold_ids:
            return 1.0 / rank
    return 0.0


def evaluate_single_example(
    example: RetrievalEvalExample,
    use_reranker: bool = False,
) -> RetrievalEvalResult:
    all_items = vector_store.get_all_items()

    retrieved_items = retrieve_chunks(
        query=example.query,
        items=all_items,
        top_k=example.top_k,
    )

    retrieved_chunks = [
        ChunkResult(
            chunk_id=item["chunk_id"],
            doc_id=item["doc_id"],
            text=item["text"],
            score=item["score"],
        )
        for item in retrieved_items
    ]

    final_chunks = retrieved_chunks
    if use_reranker:
        final_chunks = simple_rerank(retrieved_chunks, example.query)

    retrieved_chunk_ids = [chunk.chunk_id for chunk in final_chunks]
    gold_id_set = set(example.gold_chunk_ids)

    hit_at_k = compute_hit_at_k(retrieved_chunk_ids, gold_id_set)
    recall_at_k = compute_recall_at_k(retrieved_chunk_ids, gold_id_set)
    reciprocal_rank = compute_reciprocal_rank(retrieved_chunk_ids, gold_id_set)

    return RetrievalEvalResult(
        query=example.query,
        gold_chunk_ids=example.gold_chunk_ids,
        retrieved_chunk_ids=retrieved_chunk_ids,
        hit_at_k=hit_at_k,
        recall_at_k=round(recall_at_k, 4),
        reciprocal_rank=round(reciprocal_rank, 4),
    )


def evaluate_dataset(
    examples: List[RetrievalEvalExample],
    use_reranker: bool = False,
) -> RetrievalEvalSummary:
    results = [
        evaluate_single_example(example, use_reranker=use_reranker)
        for example in examples
    ]

    num_examples = len(results)
    if num_examples == 0:
        return RetrievalEvalSummary(
            num_examples=0,
            avg_hit_at_k=0.0,
            avg_recall_at_k=0.0,
            mrr=0.0,
            results=[],
        )

    avg_hit_at_k = sum(result.hit_at_k for result in results) / num_examples
    avg_recall_at_k = sum(result.recall_at_k for result in results) / num_examples
    mrr = sum(result.reciprocal_rank for result in results) / num_examples

    return RetrievalEvalSummary(
        num_examples=num_examples,
        avg_hit_at_k=round(avg_hit_at_k, 4),
        avg_recall_at_k=round(avg_recall_at_k, 4),
        mrr=round(mrr, 4),
        results=results,
    )


def compare_retrieval_modes(
    examples: List[RetrievalEvalExample],
) -> RetrievalComparisonSummary:
    retrieval_only = evaluate_dataset(examples, use_reranker=False)
    retrieval_with_rerank = evaluate_dataset(examples, use_reranker=True)

    return RetrievalComparisonSummary(
        retrieval_only=retrieval_only,
        retrieval_with_rerank=retrieval_with_rerank,
    )