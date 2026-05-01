import time
import requests

API_URL = "http://127.0.0.1:8000/query"

queries = [
    "What is RAG?",
    "How does hybrid retrieval work?",
    "What is reranking?",
]

def main():
    latencies = []

    for q in queries:
        start = time.perf_counter()

        response = requests.post(
            API_URL,
            json={
                "query": q,
                "top_k": 3,
                "debug": True
            }
        )

        elapsed = time.perf_counter() - start
        latencies.append(elapsed)

        print("=" * 60)
        print("Query:", q)
        print("Status:", response.status_code)
        print("Latency:", round(elapsed * 1000, 2), "ms")

    print("\nAverage latency:", round(sum(latencies) / len(latencies) * 1000, 2), "ms")

if __name__ == "__main__":
    main()