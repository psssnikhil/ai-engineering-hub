# Reference Project 1: Enterprise RAG Assistant

A complete, production-grade Enterprise RAG application with dense vector indexing, multi-provider LLM gateways (OpenAI + Anthropic fallback), inline document citations, and automated LLM-as-a-Judge quality evaluation.

## Architecture

- `retriever.py`: OpenAI Embeddings (`text-embedding-3-small`) & Cosine Vector Search.
- `evaluator.py`: Automated LLM-as-a-Judge evaluation harness for faithfulness scoring.
- `main.py`: Interactive CLI and REST API server via FastAPI.
- `labs.common.gateway`: Pluggable Multi-Provider LLM Gateway.

## Quick Start

```bash
cd labs/projects/enterprise_rag_system
pip install -r requirements.txt
export OPENAI_API_KEY="sk-..."

# Run CLI mode
python -m labs.projects.enterprise_rag_system.main

# Run REST API mode
python -m labs.projects.enterprise_rag_system.main --serve
```
Then visit: `http://127.0.0.1:8000/query?q=What+is+required+for+production+deployments%3F`
