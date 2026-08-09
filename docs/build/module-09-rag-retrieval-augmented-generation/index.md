---
title: "06. RAG: Retrieval-Augmented Generation"
phase: Build
module_id: module-09
---

# 06. RAG: Retrieval-Augmented Generation

Master RAG systems from fundamental chunking and embeddings to hybrid vector-sparse search, re-ranking, graph RAG, and production evaluation.

<div class="lesson-meta">
  <span class="badge badge--module">Course 06</span>
  <span class="badge badge--intermediate">⚡ Intermediate → Advanced</span>
  <span class="badge">⏱️ 11 lessons · ~18h</span>
</div>

---

## 🏗️ Enterprise Modular RAG Pipeline Architecture

```mermaid
flowchart TD
    classDef client fill:#eef2ff,stroke:#6366f1,stroke-width:2px;
    classDef ingest fill:#f0fdf4,stroke:#10b981,stroke-width:2px;
    classDef vector fill:#fff7ed,stroke:#f59e0b,stroke-width:2px;
    classDef rank fill:#fdf2f8,stroke:#f43f5e,stroke-width:2px;
    classDef gen fill:#f5f3ff,stroke:#8b5cf6,stroke-width:2px;

    subgraph Ingestion["1. Document Ingestion Pipeline"]
        Docs["Raw Documents (PDF, HTML, MD)"]:::ingest --> Chunking["Semantic Chunking"]:::ingest
        Chunking --> Embedder["Embedding Model (Dense Vectors)"]:::ingest
        Embedder --> VectorDB[("Vector Database (HNSW / Hybrid)")]:::vector
    end

    subgraph Retrieval["2. Query Expansion & Retrieval"]
        UserQuery["User Query"]:::client --> Expander["Query Expansion / Hypothetical Doc (HyDE)"]:::client
        Expander --> DenseSearch["Dense Vector Search"]:::vector
        Expander --> SparseSearch["BM25 / Keyword Search"]:::vector
        DenseSearch & SparseSearch --> RRF["Reciprocal Rank Fusion (RRF)"]:::rank
        RRF --> Reranker["Cross-Encoder Re-Ranker"]:::rank
    end

    subgraph Generation["3. Context Compression & Generation"]
        Reranker --> Compressor["Context Compression / Selection"]:::gen
        Compressor --> Prompt["Augmented System Prompt"]:::gen
        Prompt --> LLM["LLM Generation"]:::gen
        LLM --> Response["Grounded Answer + Citations"]:::client
    end
```

---

## 📚 Course Lessons

| # | Lesson Title | Duration | Level | Core Concept |
|---|--------------|----------|-------|--------------|
| 1 | [Introduction to RAG Systems](lessons/01-introduction-to-rag.md) | 50 min | <span class="badge badge--beginner">🟢 Beginner</span> | Retrieve-then-generate paradigm, parametric vs non-parametric memory |
| 2 | [Vector Databases & Embeddings](lessons/02-vector-databases.md) | 55 min | <span class="badge badge--intermediate">⚡ Intermediate</span> | Embedding spaces, distance metrics (Cosine, L2, Inner Product) |
| 3 | [Chunking Strategies](lessons/03-chunking-strategies.md) | 50 min | <span class="badge badge--intermediate">⚡ Intermediate</span> | Fixed-size, sentence, semantic, hierarchical chunking |
| 4 | [Retrieval Methods](lessons/04-Retrieval-Methods.md) | 55 min | <span class="badge badge--intermediate">⚡ Intermediate</span> | Dense retrieval, sparse keyword search, metadata filtering |
| 5 | [Building a Basic RAG System](lessons/05-Building-a-Basic-RAG-System.md) | 60 min | <span class="badge badge--intermediate">⚡ Intermediate</span> | End-to-end Python script with Chroma/FAISS and OpenAI/Anthropic |
| 6 | [Advanced RAG Techniques](lessons/06-Advanced-RAG-Techniques.md) | 55 min | <span class="badge badge--advanced">🔥 Advanced</span> | Parent-document retrieval, sentence window retrieval, HyDE |
| 7 | [Hybrid Search](lessons/07-Hybrid-Search.md) | 50 min | <span class="badge badge--intermediate">⚡ Intermediate</span> | Combining BM25 sparse + Dense vector search via Reciprocal Rank Fusion |
| 8 | [RAG Evaluation Metrics](lessons/08-RAG-Evaluation-Metrics.md) | 55 min | <span class="badge badge--advanced">🔥 Advanced</span> | Ragas triad: Faithfulness, Answer Relevance, Context Precision |
| 9 | [Agentic RAG](lessons/09-Agentic-RAG.md) | 60 min | <span class="badge badge--advanced">🔥 Advanced</span> | Self-RAG, Corrective RAG (CRAG), dynamic query routing |
| 10 | [RAG in Production](lessons/10-RAG-in-Production.md) | 65 min | <span class="badge badge--advanced">🔥 Advanced</span> | Caching, streaming, multi-tenancy, rate limits, latency optimization |
| 11 | [Graph RAG and Knowledge Graphs](lessons/11-graph-rag-and-knowledge-graphs.md) | 60 min | <span class="badge badge--advanced">🔥 Advanced</span> | Entity extraction, knowledge graph indexing, hybrid Graph+Vector RAG |

---

👉 **Get Started:** [Lesson 01 · Introduction to RAG Systems](lessons/01-introduction-to-rag.md)
