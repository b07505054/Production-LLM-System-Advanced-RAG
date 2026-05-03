import { useState } from "react";
import { Button, ScrollView, Text, TextInput, View } from "react-native";

const BASE_URL = "http://192.168.1.182:8000";
const QUERY_URL = `${BASE_URL}/query`;
const EVAL_URL = `${BASE_URL}/evaluate`;

export default function HomeScreen() {
  const [query, setQuery] = useState("What is RAG?");
  const [results, setResults] = useState<string[]>([]);
  const [latency, setLatency] = useState("Not tested yet");
  const [serverLatency, setServerLatency] = useState("");
  const [status, setStatus] = useState("Ready");
  const [cacheHit, setCacheHit] = useState<boolean | null>(null);
  const [bypassCache, setBypassCache] = useState(false);
  const [useReranker, setUseReranker] = useState(false);
  const [evalResult, setEvalResult] = useState("");
  const [evalMetrics, setEvalMetrics] = useState<any | null>(null);

  async function runQuery() {
    setStatus("Querying backend...");
    setResults([]);
    setCacheHit(null);

    const finalQuery = bypassCache ? `${query} ${Date.now()}` : query;
    const start = performance.now();

    try {
      const res = await fetch(QUERY_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: finalQuery,
          top_k: 3,
          use_reranker: useReranker,
          debug: true,
        }),
      });

      const data = await res.json();
      const end = performance.now();

      setLatency(`${(end - start).toFixed(2)} ms`);

      if (!res.ok) {
        setStatus("Query error");
        setResults([JSON.stringify(data)]);
        return;
      }

      if (data.retrieved_chunks) {
        const texts = data.retrieved_chunks.map((c: any) => {
          const score = c.score !== undefined ? `score=${c.score}` : "score=N/A";
          return `${score} | ${c.text}`;
        });
        setResults(texts);
      }

      if (data.latency_ms !== undefined) {
        setServerLatency(`${Number(data.latency_ms).toFixed(2)} ms`);
      }

      if (data.metrics?.cache_hit !== undefined) {
        setCacheHit(data.metrics.cache_hit);
      }

      setStatus("Completed");
    } catch (err: any) {
      console.error(err);
      setStatus("Query error");
      setResults([String(err)]);
    }
  }

  async function runEval() {
    setEvalResult("");
    setEvalMetrics(null);
    try {
      const res = await fetch(EVAL_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          dataset_path: "data/eval/retrieval_eval_dataset.jsonl",
          load_demo_data: true,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        setStatus("Eval error");
        setEvalResult(JSON.stringify(data, null, 2));
        return;
      }

      setStatus("Eval completed");

      const summary = data.summary ?? data;
      setEvalMetrics(summary);
    } catch (err: any) {
      console.error(err);
      setStatus("Eval error");
      setEvalResult(String(err));
    }
  }

  return (
    <ScrollView
      contentContainerStyle={{
        padding: 24,
        backgroundColor: "#111827",
        minHeight: "100%",
      }}
    >
      <Text style={{ fontSize: 28, fontWeight: "bold", color: "white" }}>
        Mobile RAG Lite
      </Text>

      <Text style={{ marginTop: 8, color: "white" }}>
        Backend: ONNX INT8 RAG
      </Text>

      <TextInput
        placeholder="Enter query..."
        placeholderTextColor="#aaa"
        value={query}
        onChangeText={setQuery}
        style={{
          marginTop: 20,
          padding: 12,
          borderRadius: 8,
          backgroundColor: "#1f2937",
          color: "white",
        }}
      />

      <View style={{ marginTop: 16 }}>
        <Button title="Run Query" onPress={runQuery} />
      </View>

      <View style={{ marginTop: 12 }}>
        <Button
          title={useReranker ? "Reranker: ON" : "Reranker: OFF"}
          onPress={() => setUseReranker(!useReranker)}
        />
      </View>

      <View style={{ marginTop: 12 }}>
        <Button
          title={bypassCache ? "Bypass Cache: ON" : "Bypass Cache: OFF"}
          onPress={() => setBypassCache(!bypassCache)}
        />
      </View>

      <View style={{ marginTop: 12 }}>
        <Button title="Run Evaluation" onPress={runEval} />
      </View>

      <Text style={{ marginTop: 20, color: "white" }}>
        Status: {status}
      </Text>

      <Text style={{ marginTop: 10, color: "white" }}>
        Client Latency: {latency}
      </Text>

      <Text style={{ marginTop: 10, color: "white" }}>
        Server Latency: {serverLatency || "N/A"}
      </Text>

      <Text style={{ marginTop: 10, color: "white" }}>
        Mode: {cacheHit === true ? "Cache Hit" : cacheHit === false ? "Cold Query" : "N/A"}
      </Text>

      <Text style={{ marginTop: 10, color: "white" }}>
        Cache Control: {bypassCache ? "Bypass Cache" : "Use Cache"}
      </Text>

      <Text style={{ marginTop: 10, color: "white" }}>
        Reranker: {useReranker ? "Enabled" : "Disabled"}
      </Text>

      <View style={{ marginTop: 20 }}>
        <Text style={{ color: "white", fontWeight: "bold", marginBottom: 8 }}>
          Retrieved Results
        </Text>

        {results.map((r, i) => (
          <Text key={i} style={{ color: "white", marginBottom: 8 }}>
            {i + 1}. {r}
          </Text>
        ))}
      </View>

      {evalMetrics && (
        <View style={{ marginTop: 20 }}>
          <Text style={{ color: "white", fontWeight: "bold", marginBottom: 12 }}>
            Evaluation Result
          </Text>

          <View
            style={{
              padding: 14,
              borderRadius: 10,
              backgroundColor: "#1f2937",
            }}
          >
            <Text style={{ color: "white", fontSize: 16, marginBottom: 8 }}>
              Examples: {evalMetrics.retrieval_only?.num_examples ?? "N/A"}
            </Text>

            <Text style={{ color: "white", fontSize: 16, marginBottom: 8 }}>
              Hit@K: {evalMetrics.retrieval_only?.avg_hit_at_k ?? "N/A"}
            </Text>

            <Text style={{ color: "white", fontSize: 16, marginBottom: 8 }}>
              Recall@K: {evalMetrics.retrieval_only?.avg_recall_at_k ?? "N/A"}
            </Text>

            <Text style={{ color: "white", fontSize: 16 }}>
              MRR: {evalMetrics.retrieval_only?.mrr ?? "N/A"}
            </Text>
          </View>
        </View>
      )}

      {evalResult.length > 0 && (
        <Text style={{ color: "white", marginTop: 20 }}>
          {evalResult}
        </Text>
      )}
    </ScrollView>
  );
}