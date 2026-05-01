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
            "title": "RAG Overview",
            "text": (
                "RAG stands for Retrieval-Augmented Generation. A RAG system first retrieves "
                "relevant documents from a knowledge base, then uses those documents as context "
                "to generate a grounded answer. This improves factuality because the answer is "
                "based on retrieved evidence instead of relying only on model memory."
            ),
        },
        {
            "doc_id": "doc_002",
            "title": "Mobile RAG Goal",
            "text": (
                "Mobile RAG adapts retrieval-augmented generation for mobile and edge environments. "
                "The goal is to support low-latency question answering with limited memory, limited "
                "compute, and unstable network conditions. A mobile RAG demo should avoid manual "
                "document ingestion and should load a prepared local corpus automatically."
            ),
        },
        {
            "doc_id": "doc_003",
            "title": "Hybrid Retrieval",
            "text": (
                "Hybrid retrieval combines keyword-based search, such as BM25, with vector similarity "
                "search from embeddings. Keyword search is strong for exact terms, while vector search "
                "captures semantic similarity. Combining both methods can improve recall and make the "
                "retrieval system more robust."
            ),
        },
        {
            "doc_id": "doc_004",
            "title": "Reranking",
            "text": (
                "Reranking improves retrieval quality by reordering candidate chunks after the initial "
                "retrieval step. A fast retriever first returns a broader set of candidates, and a "
                "stronger reranker scores them more carefully. This often improves top-ranked evidence "
                "quality before answer generation."
            ),
        },
        {
            "doc_id": "doc_005",
            "title": "Edge Latency",
            "text": (
                "Edge RAG systems must measure latency carefully because mobile users expect fast "
                "responses. Useful latency metrics include retrieval latency, reranking latency, "
                "generation latency, total response latency, and cache-hit latency. These metrics help "
                "identify which stage creates the largest bottleneck."
            ),
        },
        {
            "doc_id": "doc_006",
            "title": "Cache Optimization",
            "text": (
                "Caching can reduce repeated query latency in a mobile RAG system. If a user asks a "
                "similar question more than once, the system can reuse a previous retrieval or answer "
                "result instead of recomputing the full pipeline. Cache hit rate and cache-hit latency "
                "are important production metrics."
            ),
        },
        {
            "doc_id": "doc_007",
            "title": "Memory Footprint",
            "text": (
                "Mobile and edge deployment require careful memory management. Embedding models, vector "
                "indexes, cached responses, and retrieved chunks all consume memory. A production-ready "
                "mobile RAG system should report vector store size, number of chunks, cache size, and "
                "estimated memory footprint."
            ),
        },
        {
            "doc_id": "doc_008",
            "title": "Offline Retrieval",
            "text": (
                "Offline retrieval allows a mobile RAG demo to answer questions without depending on a "
                "live ingestion API or external database. The system can preload a small local corpus "
                "during startup and retrieve from an in-memory or persisted local vector store."
            ),
        },
        {
            "doc_id": "doc_009",
            "title": "Grounded Answers",
            "text": (
                "A grounded RAG answer should be supported by retrieved chunks. The system should return "
                "citations, retrieved evidence, and debug information so developers can inspect whether "
                "the answer is actually based on the selected context."
            ),
        },
        {
            "doc_id": "doc_010",
            "title": "Mobile Demo Workflow",
            "text": (
                "A good mobile RAG demo starts the backend server, automatically loads a prepared demo "
                "corpus, accepts questions from a mobile client, retrieves relevant chunks, generates a "
                "grounded answer, and reports latency metrics for each request."
            ),
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