# Production LLM System (Advanced RAG)

A production-style Retrieval-Augmented Generation (RAG) system with:

- Multi-document ingestion
- Dense vector retrieval
- Cross-encoder reranking
- Evaluation pipeline
- Query caching
- Monitoring & observability

---

## Overview

This project demonstrates how to build a **production-oriented retrieval system**, focusing on:

- Retrieval quality (evaluation metrics)
- System performance (latency + caching)
- Observability (monitoring endpoints)

Unlike a simple chatbot, this system emphasizes **traceability, debuggability, and measurable performance**.

---

## Architecture

Documents
↓
Chunking
↓
Embedding
↓
Vector Store
↓

Query
↓
Dense Retrieval (Top-K)
↓
Cross-Encoder Reranker
↓
Answer Generation
↓
Monitoring / Evaluation


---

## Features

### Retrieval Pipeline
- Semantic search using embeddings
- Top-k document retrieval
- Cross-encoder reranking (second-stage ranking)

### Evaluation
- Hit@k, Recall@k, MRR
- Retrieval-only vs reranked comparison
- API-based evaluation endpoint

### Performance & Observability
- Query caching (cache hit / miss)
- Stage-level latency tracking:
  - retrieval
  - reranking
  - generation
- Monitoring endpoints:
  - `/monitoring/logs`
  - `/monitoring/stats`

---

## System Design Highlights

- **Modular retrieval architecture**  
  Decoupled ingestion, retrieval, reranking, caching, evaluation, and monitoring layers enable independent upgrades.

- **Two-stage retrieval design**  
  Dense embedding retrieval for fast recall, followed by cross-encoder reranking for precision.

- **Latency-aware serving path**  
  Stage-level latency tracking allows analysis of retrieval vs reranking cost. Cache enables early exit for repeated queries.

- **Built-in observability**  
  Monitoring endpoints expose cache hit rate, latency metrics, and query logs for system inspection.

- **Evaluation as a first-class component**  
  Retrieval performance is measurable through Hit@k, Recall@k, and MRR via API or offline scripts.

- **Debug-friendly API design**  
  Query responses optionally include retrieved chunks, reranked chunks, and detailed metrics.

---

## Demo (Step-by-step)

### 1. Start server

```bash
uvicorn app.main:app --reload
```
2. Clear state
```bash
curl -X POST http://127.0.0.1:8000/store/clear
```
4. Ingest documents
```bash
curl -X POST "http://127.0.0.1:8000/ingest" -H "Content-Type: application/json" -d "{\"documents\":[{\"doc_id\":\"doc_001\",\"title\":\"Evaluation Principles\",\"text\":\"Evaluation is important in production RAG because it measures whether retrieved evidence is relevant, grounded, and useful for answering user questions. It helps teams verify answer quality instead of relying on intuition.\"},{\"doc_id\":\"doc_002\",\"title\":\"System Quality Notes\",\"text\":\"System quality depends on reliability, latency, and consistent performance over time.\"},{\"doc_id\":\"doc_003\",\"title\":\"Monitoring and Latency\",\"text\":\"Monitoring helps track latency and cache hit rate, but does not directly measure answer correctness.\"}]}"
```
6. Query WITHOUT reranking
```bash
curl -X POST "http://127.0.0.1:8000/query" -H "Content-Type: application/json" -d "{\"query\":\"Why is evaluation important for answer quality in production systems?\",\"top_k\":3,\"use_reranker\":false,\"debug\":true}"
```
8. Query WITH reranking
```bash
curl -X POST "http://127.0.0.1:8000/query" -H "Content-Type: application/json" -d "{\"query\":\"Why is evaluation important for answer quality in production systems?\",\"top_k\":3,\"use_reranker\":true,\"debug\":true}"
```
10. Cache hit (repeat query)
```bash
curl -X POST "http://127.0.0.1:8000/query" -H "Content-Type: application/json" -d "{\"query\":\"Why is evaluation important for answer quality in production systems?\",\"top_k\":3,\"use_reranker\":true,\"debug\":true}"
```
## Performance

The system demonstrates the trade-off between fast retrieval and accurate reranking.

Mode	Retrieval ms	Rerank ms	Total ms	Cache Hit	Notes
Retrieval only	~21 ms	0 ms	~21 ms	No	Fast semantic retrieval baseline
Retrieval + reranker	~14 ms	~60 ms	~75 ms	No	Cross-encoder reranking improves ranking quality
Cached query	0 ms	0 ms	~0 ms	Yes	Instant response from cache
Monitoring Snapshot
Total queries: 7
Cache hit rate: 42.86%
Avg retrieval latency: 11.54 ms
Avg rerank latency: 33.53 ms
Avg total latency: 45.18 ms
## Monitoring
Logs
```bash
curl "http://127.0.0.1:8000/monitoring/logs?limit=10"
```
Tracks:

query
cache hit
reranker usage
latency breakdown
Stats
```bash
curl http://127.0.0.1:8000/monitoring/stats
```
## Evaluation
```bash
curl -X POST "http://127.0.0.1:8000/evaluate" -H "Content-Type: application/json" -d "{\"dataset_path\":\"data/eval/retrieval_eval_dataset.jsonl\",\"load_demo_data\":true}"
```
## Metrics:

- Hit@k
- Recall@k
- MRR
## Key Insights
- Dense retrieval is fast but may not rank results optimally
- Cross-encoder reranking improves semantic ordering
- Caching reduces repeated query latency to near zero
- Monitoring enables visibility into system behavior
## Tech Stack
- FastAPI
- Python
- SentenceTransformers
- Cross-Encoder (MiniLM)
- In-memory vector store
- Custom evaluation pipeline
## Future Improvements
- Hard negative mining for evaluation dataset
- Persistent vector database (FAISS / Qdrant)
- Distributed retrieval architecture
- Integration with LLM-based answer generation
