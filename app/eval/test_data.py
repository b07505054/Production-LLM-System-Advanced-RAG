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
            "title": "Evaluation Principles",
            "text": "Evaluation is important in production RAG because it measures whether retrieved evidence is relevant, grounded, and useful for answering user questions. It helps teams verify answer quality instead of relying on intuition.",
        },
        {
            "doc_id": "doc_002",
            "title": "System Quality Notes",
            "text": "System quality depends on reliability, latency, uptime, and consistent performance over time. Teams often measure service quality using operational indicators and user-facing outcomes.",
        },
        {
            "doc_id": "doc_003",
            "title": "Monitoring and Latency",
            "text": "Monitoring helps teams track latency, cache hit rate, and failures. These metrics are important for production systems, but they do not directly measure whether answers are correct or well grounded.",
        },
        {
            "doc_id": "doc_004",
            "title": "Answer Quality Signals",
            "text": "Answer quality can be affected by response clarity, user satisfaction, formatting, and perceived usefulness. These signals are helpful but may not prove that retrieved evidence actually supports the answer.",
        },
        {
            "doc_id": "doc_005",
            "title": "Retrieval Grounding",
            "text": "Grounding means verifying that an answer is supported by the retrieved evidence. In RAG systems, grounding checks whether the selected context actually justifies the generated response.",
        },
        {
            "doc_id": "doc_006",
            "title": "Evidence Relevance",
            "text": "Relevant evidence improves answer quality by providing useful context. Systems often retrieve relevant information to enhance responses, but relevance does not guarantee correctness.",
        },
        {
            "doc_id": "doc_007",
            "title": "Evaluation vs Quality",
            "text": "Evaluation helps measure answer quality and system performance, but not all evaluation metrics directly verify whether retrieved evidence supports the answer.",
        },
        {
            "doc_id": "doc_008",
            "title": "Grounding vs Relevance",
            "text": "Grounding ensures that answers are supported by retrieved evidence, whereas relevance only indicates that the information is related to the query.",
        },
        {
            "doc_id": "doc_009",
            "title": "Fake Grounding",
            "text": "Grounding refers to ensuring that retrieved documents are relevant to the query and improve answer quality.",
        }
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