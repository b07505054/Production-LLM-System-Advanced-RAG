# Mobile RAG Lite: Edge-Oriented RAG System

## Overview

This project upgrades a production-style RAG system into a mobile-integrated, edge-oriented AI system.

The goal is to evaluate how a RAG pipeline behaves under constrained-device assumptions, including limited compute, limited memory, mobile network latency, and the need for low-latency retrieval.

The system includes:

- FastAPI RAG backend
- ONNX INT8 embedding inference
- Query-level cache
- Optional reranking
- Retrieval evaluation
- iOS mobile client
- Clientserver latency measurement
- Cold-query vs cache-hit comparison

---

## Target Deployment Scenario

This project simulates deployment for constrained mobile environments, such as:

- iPhone SE-class devices
- Budget Android phones
- CPU-first execution
- Limited memory and battery
- Unstable mobile network
- Need for fast user-facing response

The current implementation is a hybrid mobile-edge architecture:

iOS Client
   ↓
FastAPI Backend
   ↓
ONNX INT8 Embedder
   ↓
Vector Retrieval + Cache + Optional Reranker
   ↓
Evaluation Metrics

The system is not yet fully on-device. ONNX inference currently runs on the backend. A future upgrade will move the embedding model fully on-device using a bare workflow and ONNX Runtime Mobile.

---

## Key Features

### 1. Mobile RAG Client

Built an iOS client using Expo  React Native.

The mobile UI supports:

- Query input
- Backend RAG query execution
- Retrieved result display
- Client latency measurement
- Server latency measurement
- Cache hit  cold query mode display
- Cache bypass toggle
- Reranker toggle
- Evaluation trigger and metric display

### 2. ONNX INT8 Embedding Backend

The embedding model was optimized from PyTorch into ONNX and then quantized to INT8.

Pipeline:

SentenceTransformer
   ↓
ONNX FP32
   ↓
ONNX INT8
   ↓
FastAPI Embedder

Benchmark result:

Backend: Cold Query Avg Latency
ONNX FP32: ~13.14 ms
ONNX INT8: ~10.90 ms

INT8 quantization reduced backend embedding latency by approximately 17%.

### 3. Cache-Aware RAG Optimization

The system exposes both cold-query and cache-hit behavior.

Example result:

Mode: Server Latency
Cold Query: ~100 ms+
Cache Hit: ~0.02 ms

Cache hits bypass retrieval and generation, reducing repeated-query cost.

### 4. Retrieval Evaluation

The backend includes an evaluation endpoint for retrieval quality.

Metrics include:

- Hit@K
- Recall@K
- MRR

The mobile UI can trigger evaluation and display summarized metrics.

Example:

Examples: 9
Hit@K: 0.4444
Recall@K: 0.4444
MRR: 0.1991

---

## Development Strategy

This project was developed using a step-by-step validation approach.

### Step 1: Retrieval Correctness

Before optimizing latency, the retrieval pipeline was validated using Hit@K, Recall@K, and MRR.

### Step 2: Cold-Start Optimization

A cold-start latency issue was identified where the first query took over 20 seconds due to lazy model initialization.

Solution:

- Added embedding model warmup during server startup

Result:

First-query latency reduced from ~21 seconds to normal query latency.

### Step 3: Cache Benchmarking

Implemented two-round benchmarking:

- Round 1: cold query
- Round 2: cache hit

This verified that repeated queries could bypass retrieval and return near-zero server latency.

### Step 4: ONNX INT8 Optimization

Converted the embedding model to ONNX and applied INT8 quantization to reduce inference cost.

### Step 5: Mobile Integration

Built an iOS mobile client to test real-device latency and query behavior.

### Step 6: Evaluation Integration

Connected the evaluation endpoint to the mobile UI to expose retrieval quality metrics.

---

## Mobile Demo

The iOS demo shows:

- Query execution
- Retrieved chunks
- Client latency
- Server latency
- Cache hit  cold query mode
- Cache bypass control
- Reranker toggle
- Evaluation metrics

Example flow:

1. Enter query
2. Run query
3. View retrieved results
4. Compare clientserver latency
5. Repeat query to observe cache hit
6. Toggle cache bypass for cold-query testing
7. Run evaluation

---

## Technical Stack

### Backend

- Python
- FastAPI
- ONNX Runtime
- Sentence Transformers
- INT8 quantization
- Vector retrieval
- Query cache
- Retrieval evaluation

### Mobile

- React Native
- Expo Dev Client
- iOS real-device testing
- Mobile latency instrumentation

---

## Current Limitation

The current system is a hybrid architecture:

Mobile client + optimized backend

ONNX INT8 inference runs on the backend, not directly on the iPhone.

This was a deliberate engineering trade-off because Expo managed workflow has limitations with native ONNX Runtime modules on iOS.

---

## Future Work

Planned upgrades:

- Move ONNX embedding inference fully on-device
- Use bare React Native  Expo prebuild workflow
- Add local vector store on iPhone
- Add memory footprint measurement
- Add model size comparison
- Add hardware-aware runtime benchmarking
- Evaluate latency vs quality trade-offs with reranking enabled

---

## Engineering Lessons

A major challenge was iOS native build instability when attempting to integrate ONNX Runtime directly into Expo managed workflow.

Key lesson:

For mobile native ML systems, build pipeline stability must be validated before adding heavy native dependencies.

The project was reset into a clean iOS baseline and rebuilt incrementally.

This improved debuggability and avoided mixing app logic errors with native build-chain issues.

---

## Resume Summary

Built a mobile-integrated, edge-oriented RAG system with ONNX INT8-optimized embeddings, cache-aware latency benchmarking, optional reranking, retrieval evaluation, and an iOS client for real-device latency measurement.

## Demo

### 🎥 Full Demo Video (Download)
[Download Demo Video](Production-LLM-System-Advanced-RAG/mobile-rag
/assets/)

> Demonstrates cold-query vs cache latency, reranking impact, and evaluation metrics on a mobile-integrated RAG system.
