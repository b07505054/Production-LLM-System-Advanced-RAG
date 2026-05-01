import time
import requests

API_URL = "http://127.0.0.1:8000/query"

queries = [
    "What is RAG?",
    "What is Mobile RAG?",
    "How does hybrid retrieval work?",
    "What is reranking?",
    "Why is latency important for edge RAG?",
    "How does caching help mobile RAG?",
    "What is offline retrieval?",
]

def main():
    successful_latencies = []

    for round_idx in range(2):
        print("\n" + "=" * 70)
        print(f"ROUND {round_idx + 1}")
        print("=" * 70)

        for q in queries:
            start = time.perf_counter()

            response = requests.post(
                API_URL,
                json={
                    "query": q,
                    "top_k": 3,
                    "use_reranker": False,
                    "debug": True,
                },
            )

            elapsed_ms = (time.perf_counter() - start) * 1000

            print("-" * 70)
            print("Query:", q)
            print("Client latency:", round(elapsed_ms, 2), "ms")

            if response.status_code != 200:
                print("Error:", response.text)
                continue

            data = response.json()

            if round_idx == 0:
                successful_latencies.append(elapsed_ms)

            print("Server latency:", data.get("latency_ms"), "ms")
            print("Cache hit:", data.get("metrics", {}).get("cache_hit"))

    print("\n" + "=" * 70)
    print("Cold query summary (Round 1 only)")

    if successful_latencies:
        avg_latency = sum(successful_latencies) / len(successful_latencies)
        print("Average latency:", round(avg_latency, 2), "ms")
        print("Min latency:", round(min(successful_latencies), 2), "ms")
        print("Max latency:", round(max(successful_latencies), 2), "ms")
if __name__ == "__main__":
    main()