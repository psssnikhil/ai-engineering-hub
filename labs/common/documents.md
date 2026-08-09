# Enterprise Knowledge Base & Reference Documents

This document serves as the standardized sample dataset for `labs/projects/` across RAG, Hybrid Search, Evals, and Agentic workflows.

---

## Document 1: Production RAG Architecture & Vector Search Guidelines

Retrieval-Augmented Generation (RAG) bridges external knowledge stores with Large Language Models without requiring full model retrain loops. A production RAG pipeline consists of five key stages:
1. **Document Ingestion & Chunking**: Splitting raw documents into semantic chunks (e.g., 256–512 tokens) preserving heading structures and section boundaries.
2. **Dense Vector Embeddings**: Generating high-dimensional vector representations using models such as `text-embedding-3-small` (1536 dimensions) or `bge-large-en-v1.5`.
3. **Index Management**: Storing vectors in high-performance engines (Chroma, Pinecone, Qdrant, pgvector) using HNSW (Hierarchical Navigable Small World) graphs or IVF (Inverted File) indexes.
4. **Hybrid Retrieval**: Combining dense vector similarity with sparse BM25 keyword matching via Reciprocal Rank Fusion (RRF) to maximize recall and precision.
5. **Grounded Answer Generation**: Injecting top-k retrieved chunks into the prompt context along with strict citation instructions (e.g., inline source tags `[1]`, `[2]`).

---

## Document 2: ReAct Agent Framework & Tool Execution Protocol

The ReAct (Reasoning + Acting) paradigm enables LLMs to interleave step-by-step reasoning thoughts with external tool calls:
- **Thought**: The model evaluates current progress toward a goal and decides which action to take.
- **Action**: The model outputs a structured tool invocation payload (e.g., JSON function call).
- **Observation**: The runtime environment executes the tool and returns raw results back to the context.

When tool executions fail or return error messages, resilient agent loops implement observation recovery, retry budgets, and exponential backoff rather than crashing.

---

## Document 3: Model Context Protocol (MCP) Standard

Model Context Protocol (MCP) is an open standard established to unify how AI applications connect with external tools, data sources, and context servers via JSON-RPC 2.0 over standard I/O or Server-Sent Events (SSE). Key components include:
- **MCP Client**: The AI application or agent loop initiating connection and discovering capabilities.
- **MCP Server**: Lightweight service exposing resources, prompts, and executable tool schemas (`tools/list` and `tools/call`).
- **Tool Discovery**: Dynamic capability exchange allowing clients to discover new tools at runtime without hardcoded tool definitions.

---

## Document 4: Automated LLM Evaluation & CI Quality Gates

Relying solely on manual human review for LLM outputs is unscalable for production software engineering. Modern LLMOps pipelines establish automated CI quality gates using **LLM-as-a-Judge**:
- **Faithfulness Score**: Measures whether every claim in the generated output is directly supported by the retrieved context chunks (detecting hallucinations).
- **Context Relevance Score**: Evaluates whether retrieved chunks contain useful information for answering the query.
- **Answer Relevance Score**: Ensures the generated output directly addresses the user's prompt without introducing off-topic filler.

Automated evaluation suites fail build pipelines if faithfulness falls below 0.90 or hallucination rate exceeds 5%.

---

## Document 5: AI Safety, Security, & Guardrails Gateway

Production AI deployments enforce multi-layer safety guardrails to protect against adversarial prompts, data leaks, and unsafe advice:
- **Prompt Injection Defense**: Detecting direct and indirect prompt overrides before passing inputs to the LLM.
- **PII / HIPAA Redaction**: Anonymizing Personally Identifiable Information (SSN, credit cards, medical IDs) prior to external model calls.
- **Emergency Triage Classifier**: Intercepting high-stakes crisis inputs (e.g. medical emergencies) to trigger immediate escalation protocols.
- **Output Validation**: Ensuring model outputs adhere to JSON schemas and legal disclaimer requirements.
