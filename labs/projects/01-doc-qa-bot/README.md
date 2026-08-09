# Project 1: Document Q&A Bot (RAG Starter)

A production-grade reference implementation of a Document Q&A Bot with TF-IDF/Dense retrieval, inline document citations, CLI mode, and a FastAPI web endpoint.

## Features
- **Chunking & Vector Indexing**: Splits text into retrieval chunks and indexes them.
- **Inline Citations**: Grounded responses link back to exact `[doc_id:chunk_id]` references.
- **Dual Mode**: Interactive CLI or REST API server via FastAPI.

## Quick Start

```bash
cd labs/projects/01-doc-qa-bot
python main.py
```

### Run FastAPI Server

```bash
pip install -r requirements.txt
python main.py --serve
```
Then visit: `http://127.0.0.1:8000/query?q=What+is+required+for+deploying+LLM+apps%3F`
