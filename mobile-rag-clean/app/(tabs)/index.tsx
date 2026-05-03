import { useState } from "react";
import { Button, Text, TextInput, View } from "react-native";

const API_URL = "http://192.168.1.182:8000/query";

export default function HomeScreen() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<string[]>([]);
  const [latency, setLatency] = useState("Not tested yet");
  const [serverLatency, setServerLatency] = useState("");
  const [status, setStatus] = useState("Ready");
  const [cacheHit, setCacheHit] = useState<boolean | null>(null);

  async function runQuery() {
    setStatus("Querying backend...");
    setResults([]);
    setCacheHit(null);

    const start = performance.now();

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: query,
          top_k: 3,
          use_reranker: false,
          debug: true,
        }),
      });

      const data = await res.json();

      const end = performance.now();

      setLatency(`${(end - start).toFixed(2)} ms`);

      if (data.retrieved_chunks) {
        const texts = data.retrieved_chunks.map((c: any) => c.text);
        setResults(texts);
      }

      if (data.latency_ms) {
        setServerLatency(`${data.latency_ms.toFixed(2)} ms`);
      }
      
      if (data.metrics?.cache_hit !== undefined) {
        setCacheHit(data.metrics.cache_hit);
      }

      setStatus("Completed");
    } catch (err) {
      console.error(err);
      setStatus("Error");
    }
  }

  return (
    <View
      style={{
        flex: 1,
        padding: 24,
        backgroundColor: "#111827",
      }}
    >
      <Text style={{ fontSize: 28, fontWeight: "bold", color: "white" }}>
        Mobile RAG Lite
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

      <Text style={{ marginTop: 20, color: "white" }}>
        Status: {status}
      </Text>

      <Text style={{ marginTop: 10, color: "white" }}>
        Client Latency: {latency}
      </Text>

      <Text style={{ marginTop: 10, color: "white" }}>
        Server Latency: {serverLatency}
      </Text>

      <Text style={{ marginTop: 10, color: "white" }}>
        Mode: {cacheHit === true ? "Cache Hit" : cacheHit === false ? "Cold Query" : "N/A"}
      </Text>

      <View style={{ marginTop: 20 }}>
        {results.map((r, i) => (
          <Text key={i} style={{ color: "white", marginBottom: 8 }}>
            {i + 1}. {r}
          </Text>
        ))}
      </View>
    </View>
  );
}