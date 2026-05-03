import { useState } from "react";
import { Button, Text, View } from "react-native";

export default function HomeScreen() {
  const [latency, setLatency] = useState("Not tested yet");
  const [status, setStatus] = useState("Ready");

  async function runMobileRagDemo() {
    setStatus("Running mobile RAG simulation...");

    const start = performance.now();

    // Simulate on-device embedding + local retrieval workload
    await new Promise((resolve) => setTimeout(resolve, 50));

    const end = performance.now();

    setLatency(`${(end - start).toFixed(2)} ms`);
    setStatus("Completed");
  }

  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        padding: 24,
        backgroundColor: "#111827",
      }}
    >
      <Text style={{ fontSize: 30, fontWeight: "bold", color: "white" }}>
        Mobile RAG Lite
      </Text>

      <Text style={{ marginTop: 16, fontSize: 16, color: "white", textAlign: "center" }}>
        iOS demo for edge-oriented RAG latency measurement.
      </Text>

      <View style={{ marginTop: 24 }}>
        <Button title="Run Mobile RAG Demo" onPress={runMobileRagDemo} />
      </View>

      <Text style={{ marginTop: 24, fontSize: 18, color: "white" }}>
        Status: {status}
      </Text>

      <Text style={{ marginTop: 12, fontSize: 18, color: "white" }}>
        Latency: {latency}
      </Text>
    </View>
  );
}