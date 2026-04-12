from sentence_transformers import CrossEncoder

from app.schemas.query import ChunkResult


class CrossEncoderReranker:
    """
    Cross-encoder reranker for second-stage ranking.

    This reranker scores (query, chunk_text) pairs directly.
    """

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2") -> None:
        self.model = CrossEncoder(model_name)

    def rerank(self, query: str, chunks: list[ChunkResult]) -> list[ChunkResult]:
        if not chunks:
            return []

        pairs = [[query, chunk.text] for chunk in chunks]
        scores = self.model.predict(pairs)

        rescored_chunks = []
        for chunk, rerank_score in zip(chunks, scores):
            rescored_chunks.append(
                ChunkResult(
                    chunk_id=chunk.chunk_id,
                    doc_id=chunk.doc_id,
                    text=chunk.text,
                    score=float(rerank_score),
                )
            )

        rescored_chunks.sort(key=lambda c: c.score, reverse=True)
        return rescored_chunks


reranker = CrossEncoderReranker()


def simple_rerank(chunks: list[ChunkResult], query: str) -> list[ChunkResult]:
    """
    Backward-compatible interface.
    Now uses a cross-encoder reranker instead of heuristic rules.
    """
    return reranker.rerank(query=query, chunks=chunks)