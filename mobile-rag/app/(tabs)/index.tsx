import { useState } from "react";
import { Button, Text, View } from "react-native";

export default function HomeScreen() {
  const [latency, setLatency] = useState<string>("Not tested yet");

  async function runLatencyTest() {
    const start = performance.now();

    // 先模擬一次 mobile inference / retrieval workload
    await new Promise((resolve) => setTimeout(resolve, 10));

    const end = performance.now();
    setLatency(`${(end - start).toFixed(2)} ms`);
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
      <Text style={{ fontSize: 28, fontWeight: "bold", color: "white" }}>
        Mobile RAG Lite
      </Text>

      <Text style={{ marginTop: 16, fontSize: 16, color: "white" }}>
        iOS Expo demo is running.
      </Text>

      <View style={{ marginTop: 24 }}>
        <Button title="Run Mobile Latency Test" onPress={runLatencyTest} />
      </View>

      <Text style={{ marginTop: 24, fontSize: 18, color: "white" }}>
        Latency: {latency}
      </Text>
    </View>
  );
}