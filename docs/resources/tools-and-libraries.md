---
title: Complete AI Tools, Libraries & SDKs Index
description: Categorized reference directory of top open-source tools, SDKs, vector databases, serving engines, and framework documentation.
---

# 🛠 Complete AI Tools, Libraries & SDKs Index

A categorized, annotated reference directory of essential open-source libraries, SDKs, serving engines, vector databases, and official API documentations referenced throughout the handbook.

---

## ⚡ 1. LLM Serving Engines & Gateway Proxies

| Tool / SDK | Description & Focus Area | Official Link |
|------------|--------------------------|---------------|
| **vLLM** | High-throughput, memory-efficient LLM inference engine with PagedAttention and continuous batching. | [GitHub Repo](https://github.com/vllm-project/vllm) · [Docs](https://docs.vllm.ai) |
| **LiteLLM** | Lightweight proxy gateway allowing 100+ LLM APIs to be called using standard OpenAI format with cost tracking. | [GitHub Repo](https://github.com/BerriAI/litellm) |
| **Ollama** | Get up and running with local open-weight models (Llama 3, Mistral) via simple CLI and REST API. | [Official Site](https://ollama.com) |
| **Text Generation Inference (TGI)** | Hugging Face's production inference server for deploying large language models with speculative decoding. | [Hugging Face Docs](https://huggingface.co/docs/text-generation-inference) |

---

## 🤖 2. Agent Frameworks, MCP & Tool Execution

| Tool / SDK | Description & Focus Area | Official Link |
|------------|--------------------------|---------------|
| **LangGraph** | Industry-standard graph framework for building stateful, multi-agent applications with cyclic workflows. | [Docs](https://langchain-ai.github.io/langgraph/) |
| **Smolagents** | Lightweight, code-first agent framework from Hugging Face that executes Python code actions natively. | [GitHub Repo](https://github.com/huggingface/smolagents) |
| **AutoGen** | Microsoft's framework enabling multi-agent conversation, task delegation, and code execution teams. | [GitHub Repo](https://github.com/microsoft/autogen) |
| **CrewAI** | Role-playing, autonomous multi-agent framework for collaborative task execution. | [Docs](https://docs.crewai.com/) |
| **FastMCP** | High-level Python SDK for building Model Context Protocol (MCP) servers, tools, and resource providers. | [GitHub Repo](https://github.com/jlowin/fastmcp) |
| **Instructor** | Python library built on Pydantic for extracting structured, validated JSON data directly from LLM calls. | [GitHub Repo](https://github.com/jxnl/instructor) |

---

## 📚 3. RAG, Retrieval & Vector Databases

| Tool / SDK | Description & Focus Area | Official Link |
|------------|--------------------------|---------------|
| **LlamaIndex** | Data framework for connecting private data sources to LLMs with advanced RAG indexing algorithms. | [Docs](https://docs.llamaindex.ai/) |
| **Qdrant** | High-performance vector database written in Rust with vector payload filtering and hybrid BM25 search. | [Official Site](https://qdrant.tech/) |
| **Chroma** | Open-source embedding database designed for rapid local prototyping and Python/TypeScript apps. | [Docs](https://docs.trychroma.com/) |
| **Pinecone** | Managed vector database service built for high scale, low latency, and hybrid vector search. | [Docs](https://docs.pinecone.io/) |
| **pgvector** | Open-source vector similarity search extension for PostgreSQL supporting HNSW and IVFFlat indexes. | [GitHub Repo](https://github.com/pgvector/pgvector) |
| **FAISS** | Facebook AI Similarity Search library for efficient dense vector clustering and similarity matching. | [GitHub Wiki](https://github.com/facebookresearch/faiss/wiki) |
| **rank_bm25** | Python implementation of BM25 algorithms for sparse keyword retrieval and hybrid ranking. | [GitHub Repo](https://github.com/dorianbrown/rank_bm25) |

---

## 📊 4. Evaluation, Observability & Guardrails

| Tool / SDK | Description & Focus Area | Official Link |
|------------|--------------------------|---------------|
| **Ragas** | Framework for evaluating Retrieval Augmented Generation pipelines with faithfulness & recall metrics. | [Docs](https://docs.ragas.io/) |
| **Phoenix (Arize)** | Open-source AI observability platform for tracing LLM applications, agent steps, and evals. | [Docs](https://docs.arize.com/phoenix) |
| **LangSmith** | Platform for debugging, testing, evaluating, and monitoring LLM applications and agent chains. | [Docs](https://docs.smith.langchain.com/) |
| **Promptfoo** | Command-line tool and library for testing, evaluating, and red-teaming LLM prompts and guardrails. | [GitHub Repo](https://github.com/promptfoo/promptfoo) |
| **Garak** | LLM vulnerability scanner for automated prompt injection detection, jailbreaking, and safety red-teaming. | [GitHub Repo](https://github.com/NVIDIA/garak) |

---

## 🎛 5. Fine-Tuning, Quantization & Tokenization

| Tool / SDK | Description & Focus Area | Official Link |
|------------|--------------------------|---------------|
| **Unsloth** | Ultra-fast 2-5x faster LLM fine-tuning library with 80% reduced VRAM consumption. | [GitHub Repo](https://github.com/unslothai/unsloth) |
| **PEFT (Hugging Face)** | Parameter-Efficient Fine-Tuning library supporting LoRA, Prefix Tuning, and P-Tuning. | [Hugging Face Docs](https://huggingface.co/docs/peft) |
| **TRL (Hugging Face)** | Transformer Reinforcement Learning library for post-training LLMs using SFT, DPO, and PPO. | [Hugging Face Docs](https://huggingface.co/docs/trl) |
| **tiktoken** | Fast BPE tokenizer library developed by OpenAI for token counting and text encoding. | [GitHub Repo](https://github.com/openai/tiktoken) |
| **SentencePiece** | Unsupervised text tokenizer and detokenizer for neural network-based text processing. | [GitHub Repo](https://github.com/google/sentencepiece) |

---

## 📑 6. Official API Guides & Cookbooks

| Resource | Description | Official Link |
|----------|-------------|---------------|
| **OpenAI Cookbook** | Code examples, integration guides, and recipes for OpenAI APIs and embeddings. | [Cookbook Site](https://cookbook.openai.com/) |
| **Anthropic Engineering Docs** | Guides on prompt design, context engineering, tool use, and Claude API integration. | [Anthropic Docs](https://docs.anthropic.com/) |
| **Hugging Face Model Hub & Leaderboards** | Open community platform hosting 500k+ models, datasets, and MTEB leaderboard. | [Hugging Face Site](https://huggingface.co/) |
