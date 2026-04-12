from app.ingestion.chunker import chunk_text
from app.retrieval.embedder import embedder
from app.retrieval.vector_store import vector_store


def load_demo_eval_documents() -> None:
    """
    Load a small demo corpus into the current process's vector store.
    This is used for local evaluation scripts.
    """
    vector_store.clear()

    documents = [
        {
            "doc_id": "doc_001",
            "title": "Evaluation Notes",
            "text": "Evaluation is essential for measuring retrieval quality, groundedness, and latency in production RAG systems.",
        },
        {
            "doc_id": "doc_002",
            "title": "Assessment Notes",
            "text": "Assessment helps teams understand system performance, reliability, and answer quality over time.",
        },
    ]

    all_chunks = []
    for doc in documents:
        chunks = chunk_text(
            doc_id=doc["doc_id"],
            title=doc["title"],
            text=doc["text"],
            chunk_size=300,
            chunk_overlap=50,
        )
        all_chunks.extend(chunks)

    chunk_texts = [chunk["text"] for chunk in all_chunks]
    chunk_vectors = embedder.embed_texts(chunk_texts)

    items_to_store = []
    for chunk, vector in zip(all_chunks, chunk_vectors):
        item = dict(chunk)
        item["embedding"] = vector
        items_to_store.append(item)

    vector_store.add_items(items_to_store)