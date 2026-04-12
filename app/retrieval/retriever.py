import math
from typing import Dict, List

from app.retrieval.embedder import embedder


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)


def retrieve_chunks(query: str, items: List[Dict], top_k: int = 5) -> List[Dict]:
    query_vector = embedder.embed_text(query)
    scored = []

    for item in items:
        score = cosine_similarity(query_vector, item["embedding"])
        item_with_score = dict(item)
        item_with_score["score"] = round(score, 4)
        scored.append(item_with_score)

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]