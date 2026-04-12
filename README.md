# 🚀 Production LLM System (Advanced RAG)

A production-ready Retrieval-Augmented Generation (RAG) system with:

- 📄 Multi-document ingestion  
- 🔍 Dense vector retrieval  
- 🧠 Cross-encoder reranking  
- 📊 Evaluation pipeline  
- ⚡ Query caching  
- 📡 Monitoring & observability  

---

## ⚡ Quick Start

### 1. Start server

```bash
uvicorn app.main:app --reload
2. Clear state
curl -X POST http://127.0.0.1:8000/store/clear
3. Ingest documents
curl -X POST "http://127.0.0.1:8000/ingest" \
-H "Content-Type: application/json" \
-d '{
  "documents":[
    {
      "doc_id":"doc_001",
      "title":"Evaluation Principles",
      "text":"Evaluation is important in production RAG because it measures whether retrieved evidence is relevant, grounded, and useful."
    },
    {
      "doc_id":"doc_002",
      "title":"System Quality Notes",
      "text":"System quality depends on reliability, latency, and consistent performance."
    }
  ]
}'
🔍 Query Examples
Without reranking
curl -X POST "http://127.0.0.1:8000/query" \
-H "Content-Type: application/json" \
-d '{
  "query":"Why is evaluation important?",
  "top_k":3,
  "use_reranker":false,
  "debug":true
}'

👉 Expected:

Fast (~20ms)
No reranking
rerank_ms = 0
With reranking
curl -X POST "http://127.0.0.1:8000/query" \
-H "Content-Type: application/json" \
-d '{
  "query":"Why is evaluation important?",
  "top_k":3,
  "use_reranker":true,
  "debug":true
}'

👉 Expected:

Slower (~70ms)
Better ranking
rerank_ms > 0
Cache hit

Repeat the same query:

👉 Expected:

cache_hit = true
latency ≈ 0ms
retrieval skipped
🧠 Architecture
Documents
   ↓
Chunking
   ↓
Embedding
   ↓
Vector Store

Query
   ↓
Dense Retrieval (Top-K)
   ↓
Cross-Encoder Reranker
   ↓
Answer Generation
   ↓
Monitoring / Evaluation
📊 Monitoring
Logs
curl "http://127.0.0.1:8000/monitoring/logs?limit=10"

Tracks:

query
cache hit
reranker usage
latency per stage
Stats
curl http://127.0.0.1:8000/monitoring/stats

Example:

{
  "total_queries": 7,
  "cache_hit_rate": 0.42,
  "avg_retrieval_ms": 11.5,
  "avg_rerank_ms": 33.5,
  "avg_total_ms": 45.1
}
📈 Evaluation
curl -X POST "http://127.0.0.1:8000/evaluate" \
-H "Content-Type: application/json" \
-d '{
  "dataset_path":"data/eval/retrieval_eval_dataset.jsonl",
  "load_demo_data":true
}'

Metrics:

Hit@k
Recall@k
MRR
🧩 Key Insights
Dense retrieval is fast but not always optimal
Reranking improves semantic relevance
Caching reduces latency significantly
Monitoring is essential for production systems
🛠 Tech Stack
FastAPI
Python
SentenceTransformers
Cross-Encoder (MiniLM)
In-memory vector store
🔮 Future Improvements
Persistent vector DB (FAISS / Qdrant)
Distributed retrieval
Hard negative mining
Real LLM answer generation