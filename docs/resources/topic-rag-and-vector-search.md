---
title: Topic Resources — RAG & Vector Search
description: Curated papers, open-source repositories, YouTube lectures, free courses, and code references for Retrieval Augmented Generation (RAG) and Vector Databases.
---

# 📚 RAG & Vector Search — Topic Resources

Curated list of top landmark papers, open-source repositories, video series, free courses, and code references for **Retrieval Augmented Generation (RAG), Hybrid Search, Vector Databases, Reranking, and Context Engineering**.

---

## 📄 Landmark Papers & Essential Reading

| Paper / Reference | Key Takeaways & Focus | Link |
|-------------------|-----------------------|------|
| **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** *(Lewis et al., 2020)* | Foundational paper combining parametric memory (generator) with non-parametric memory (retriever). | [ArXiv Link](https://arxiv.org/abs/2005.11401) |
| **Dense Passage Retrieval (DPR)** *(Karpukhin et al., 2020)* | Proved dual-encoder dense vector retrieval outperforms traditional sparse BM25 for open-domain QA. | [ArXiv Link](https://arxiv.org/abs/2004.04906) |
| **ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction** *(Khattab et al., 2020)* | Late-interaction model preserving fine-grained token-level matching with sub-second vector search speed. | [ArXiv Link](https://arxiv.org/abs/2004.12832) |
| **Precise Zero-Shot Dense Retrieval without Relevance Labels (HyDE)** *(Gao et al., 2022)* | Hypothetical Document Embeddings — generating candidate answers first to retrieve relevant real documents. | [ArXiv Link](https://arxiv.org/abs/2212.10496) |
| **From Local to Global Retrieval-Augmented Generation (GraphRAG)** *(Edge et al., Microsoft 2024)* | Combines knowledge graph extraction with LLM community summaries for global dataset understanding. | [ArXiv Link](https://arxiv.org/abs/2404.16130) |
| **Corrective Retrieval-Augmented Generation (CRAG)** *(Yan et al., 2024)* | Evaluates document relevance dynamically and triggers web search fallbacks for low-confidence retrievals. | [ArXiv Link](https://arxiv.org/abs/2401.15884) |
| **Speculative RAG: Enhancing Retrieval-Augmented Generation via Draft Models** *(Wang et al., 2024)* | Uses a small specialist draft model to evaluate multiple document subsets in parallel for fast verification. | [ArXiv Link](https://arxiv.org/abs/2407.08223) |
| **LightRAG: Simple and Fast Knowledge Graph RAG** *(Guo et al., 2024)* | Dual-level retrieval paradigm combining entity-relation graphs with low-overhead vector search. | [ArXiv Link](https://arxiv.org/abs/2410.05779) |

---

## 💻 Top Open-Source Repositories & Vector DBs

| Repository | Description | Link |
|------------|-------------|------|
| **LlamaIndex** | The premier data framework for connecting private data sources (PDFs, DBs, Slack) to LLMs with advanced RAG. | [GitHub Repo](https://github.com/run-llama/llama_index) |
| **LangChain** | Popular framework for building context-aware reasoning applications and retrieval pipelines. | [GitHub Repo](https://github.com/langchain-ai/langchain) |
| **Qdrant** | High-performance vector database written in Rust with vector payload filtering and hybrid BM25 search. | [GitHub Repo](https://github.com/qdrant/qdrant) |
| **Chroma** | Open-source embedding database designed for easy local development and Python/TypeScript integration. | [GitHub Repo](https://github.com/chroma-core/chroma) |
| **Milvus** | Enterprise-grade cloud-native vector database built for billion-scale vector retrieval and distributed cluster setup. | [GitHub Repo](https://github.com/milvus-io/milvus) |
| **pgvector** | Open-source vector similarity search extension for PostgreSQL supporting HNSW and IVFFlat indexes. | [GitHub Repo](https://github.com/pgvector/pgvector) |
| **LanceDB** | Developer-friendly, serverless vector database built on Apache Arrow for fast columnar and multimodal search. | [GitHub Repo](https://github.com/lancedb/lancedb) |

---

## 🎥 Must-Watch YouTube Videos & Free Lectures

| Video / Playlist | Creator | Description | Link |
|------------------|---------|-------------|------|
| **Building Production RAG Applications** | DeepLearning.AI | Free short course by Jerry Liu (LlamaIndex founder) on advanced RAG patterns (sentence window, auto-merging). | [DeepLearning.AI Site](https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/) |
| **RAG Architecture & Vector Search Masterclass** | James Briggs | Step-by-step video tutorials on Pinecone, Qdrant, hybrid search, Cohere reranking, and BM25 integration. | [Search on YouTube →](https://www.youtube.com/results?search_query=James+Briggs+RAG+Architecture+%26+Vector+Search+Masterclass) |
| **RAG Triad & Evaluation** | TruLens / Arize | Video walkthroughs explaining Context Relevance, Groundedness, and Answer Relevance evaluation. | [YouTube Video](https://www.youtube.com/watch?v=0hM4-S9vW4c) |

---

## 🎓 Free Courses & Open Curricula

| Course Title | Institution / Host | Focus | Link |
|--------------|-------------------|-------|------|
| **Advanced RAG with LlamaIndex** | DeepLearning.AI | Practical hands-on training on document parsing, indexing, query routers, and reranking algorithms. | [DeepLearning.AI Course](https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/) |
| **Vector Search & Embeddings Academy** | Pinecone / Weaviate | Interactive guides covering vector distance metrics (Cosine, Dot Product, Euclidean), HNSW, and IVF index tuning. | [Weaviate Academy](https://weaviate.io/developers/academy) |
| **RAG Techniques (Open Source Hub)** | Nirant Kasliwal | Comprehensive directory of RAG strategies including Parent-Document, GraphRAG, and Multi-Vector retrieval. | [GitHub Repo](https://github.com/NirantK/awesome-rag-tutorials) |

---

## ⚙️ Code References & Hands-on Notebooks

- **[LlamaIndex Official Cookbooks](https://github.com/run-llama/llama_index/tree/main/docs/docs/examples)** — Complete Python notebooks for GraphRAG, Hybrid Search, and Re-ranking.
- **[OpenAI RAG & Embeddings Guide](https://cookbook.openai.com/examples/vector_databases/readme)** — Code recipes for chunking, batch embeddings, and similarity search.
- **[Pinecone Notebooks & Cookbook](https://github.com/pinecone-io/examples)** — Production implementations of hybrid search (sparse + dense) and multi-tenant RAG.
