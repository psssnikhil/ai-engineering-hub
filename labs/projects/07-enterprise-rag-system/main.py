"""
Enterprise RAG Assistant (CLI + FastAPI Server)
================================================
AI Engineering Hub — Reference Project 07

Uses:
  - `retriever.py`: Embeddings & Vector Similarity (with offline keyless fallback)
  - `evaluator.py`: Automated LLM Judge Quality Evals
  - `labs.common.gateway`: Multi-Provider Fallback Routing (OpenAI, Anthropic & Mock)

Usage:
  CLI Mode:    python main.py
  Web Server:  python main.py --serve (runs at http://127.0.0.1:8000)
"""

import sys
import os
from typing import Dict, Any

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from labs.common.gateway import LLMGateway

try:
    from retriever import DenseRetriever
    from evaluator import QualityEvaluator
    from config import DEFAULT_TOP_K
except ImportError:
    from .retriever import DenseRetriever
    from .evaluator import QualityEvaluator
    from .config import DEFAULT_TOP_K


class EnterpriseRAGSystem:
    def __init__(self):
        # Configure Multi-Provider Gateway (OpenAI, Anthropic, and Mock fallback)
        self.gateway = LLMGateway()
        self.retriever = DenseRetriever()
        self.evaluator = QualityEvaluator(self.gateway)

    def seed_documents(self) -> None:
        self.retriever.ingest(
            "architecture_spec.txt",
            "The Enterprise RAG System leverages dense vector indexing, multi-provider LLM gateways, "
            "and continuous LLM-as-a-Judge quality evaluation pipelines to ensure 99.9% uptime and high precision."
        )
        self.retriever.ingest(
            "deployment_guide.txt",
            "Production deployments require sliding-window rate limiting, exponential backoff retries, "
            "and automated CI quality gates that fail builds if hallucination rates exceed 5%."
        )

    def query(self, user_query: str) -> Dict[str, Any]:
        results = self.retriever.search(user_query, top_k=DEFAULT_TOP_K)
        context_str = "\n".join(f"[{c.doc_id}:chunk_{c.chunk_id}] {c.text}" for c, _ in results)

        messages = [
            {
                "role": "system",
                "content": "Answer the query based ONLY on the provided context. Cite sources inline like [doc_id:chunk_id]."
            },
            {"role": "user", "content": f"Context:\n{context_str}\n\nQuery: {user_query}"}
        ]

        response = self.gateway.generate(messages=messages, temperature=0.0)

        # Run automated quality eval
        eval_scores = self.evaluator.evaluate_groundedness(user_query, context_str, response.content)

        return {
            "query": user_query,
            "answer": response.content,
            "provider_used": response.provider_name,
            "model_used": response.model_name,
            "eval_scores": eval_scores,
            "citations": [f"{c.doc_id}:chunk_{c.chunk_id} (score: {s:.3f})" for c, s in results],
        }


def main():
    rag = EnterpriseRAGSystem()
    rag.seed_documents()

    if "--serve" in sys.argv:
        try:
            import uvicorn
            from fastapi import FastAPI

            app = FastAPI(title="Enterprise RAG System API")

            @app.get("/query")
            def query_endpoint(q: str):
                return rag.query(q)

            print("Starting FastAPI server at http://127.0.0.1:8000 ...")
            uvicorn.run(app, host="127.0.0.1", port=8000)
        except ImportError:
            print("Error: FastAPI and Uvicorn required for server mode.")
    else:
        print("=" * 60)
        print("  Enterprise RAG Assistant (Project 07)")
        print("=" * 60)
        sample_q = "What is required for production deployments?"
        print(f"\nUser Query: {sample_q}\n")
        res = rag.query(sample_q)
        print(f"Answer ({res['provider_used']} / {res['model_used']}):\n{res['answer']}\n")
        print(f"Citations: {res['citations']}")
        print(f"Eval Scores: {res['eval_scores']}")


if __name__ == "__main__":
    main()
