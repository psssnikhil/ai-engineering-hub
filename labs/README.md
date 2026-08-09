# Labs — Production-Grade Python Reference Code

Modular, reusable Python code (`.py` files only) pairing directly with the curriculum. All labs use pure Python and official SDKs (`openai`, `anthropic`).

---

## Quick Setup

```bash
cd labs
pip install -r requirements.txt

# Set your API keys (OpenAI, Anthropic, or both!)
export OPENAI_API_KEY=sk-proj-...
export ANTHROPIC_API_KEY=sk-ant-...
```

---

## Standardized Common Infrastructure

- **[`labs/common/gateway.py`](common/gateway.py)**: Multi-Provider LLM Gateway with automatic fallback routing (OpenAI $\rightarrow$ Anthropic) and extensible `BaseProvider` architecture for Ollama, Gemini, and local models.

---

## Consolidated Reference Projects (`labs/projects/`)

| Project | Location | Description |
|---------|----------|-------------|
| **1. Enterprise RAG Assistant** | [`projects/enterprise_rag_system/`](projects/enterprise_rag_system/) | Full RAG pipeline with dense vector indexing, inline citations, LLM Judge quality evaluation, CLI, and FastAPI web server. |
| **2. Autonomous Agent Platform** | [`projects/autonomous_agent_platform/`](projects/autonomous_agent_platform/) | Autonomous ReAct agent platform with multi-step reasoning, tool execution, multi-provider gateway, and markdown report synthesis. |

---

## Pure Python Labs (`labs/labs/`)

| Lab Script | Description |
|------------|-------------|
| **[`01_rag_from_scratch.py`](labs/01_rag_from_scratch.py)** | Vector embeddings retrieval and grounded generation using `LLMGateway`. |
| **[`02_agent_loop_from_scratch.py`](labs/02_agent_loop_from_scratch.py)** | ReAct tool-calling agent loop with step observation logging. |
| **[`03_eval_harness_from_scratch.py`](labs/03_eval_harness_from_scratch.py)** | Multi-metric LLM-as-a-Judge quality harness with JSON scoring. |
| **[`04_hybrid_search_reranking.py`](labs/04_hybrid_search_reranking.py)** | Hybrid keyword (BM25) + dense vector search with Reciprocal Rank Fusion (RRF). |
