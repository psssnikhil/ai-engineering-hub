"""
Document Q&A Bot (RAG Starter Project)
======================================
Build These Project #1 — AI Engineering Hub

Features:
  - Real OpenAI Embeddings (text-embedding-3-small) & Vector Retrieval
  - RAG prompt augmentation with inline citations [doc:chunk]
  - Both CLI interactive mode and FastAPI web endpoint

Usage:
  CLI Mode:    python main.py
  Web Server:  python main.py --serve (runs at http://127.0.0.1:8000)
"""

import sys
import math
import os
from dataclasses import dataclass
from typing import List, Tuple, Dict, Any
from openai import OpenAI


@dataclass
class DocumentChunk:
    doc_id: str
    chunk_id: int
    text: str
    vector: List[float]


class OpenAIRAGEngine:
    def __init__(self, embedding_model: str = "text-embedding-3-small", llm_model: str = "gpt-4o-mini"):
        self.client = OpenAI()
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        self.chunks: List[DocumentChunk] = []

    def _get_embedding(self, text: str) -> List[float]:
        res = self.client.embeddings.create(model=self.embedding_model, input=text)
        return res.data[0].embedding

    def ingest_document(self, doc_id: str, content: str, chunk_size_words: int = 40) -> None:
        words = content.split()
        chunk_idx = 1
        for i in range(0, len(words), chunk_size_words):
            chunk_text = " ".join(words[i:i + chunk_size_words])
            vector = self._get_embedding(chunk_text)
            self.chunks.append(DocumentChunk(doc_id=doc_id, chunk_id=chunk_idx, text=chunk_text, vector=vector))
            chunk_idx += 1

    @staticmethod
    def _cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        dot = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        return dot / (norm_a * norm_b) if (norm_a > 0 and norm_b > 0) else 0.0

    def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[DocumentChunk, float]]:
        q_vec = self._get_embedding(query)
        results = []
        for chunk in self.chunks:
            score = self._cosine_similarity(q_vec, chunk.vector)
            results.append((chunk, score))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def answer_query(self, query: str) -> Dict[str, Any]:
        top_chunks = self.retrieve(query, top_k=3)
        context_str = "\n".join(
            f"[{c.doc_id}:chunk_{c.chunk_id}] {c.text}" for c, _ in top_chunks
        )

        response = self.client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a production Document Q&A Assistant. Answer the query using ONLY "
                        "the provided context. Include inline citations like [doc_id:chunk_id] for every key fact."
                    )
                },
                {"role": "user", "content": f"Context:\n{context_str}\n\nQuery: {query}"}
            ],
            temperature=0.0,
        )

        return {
            "query": query,
            "answer": response.choices[0].message.content,
            "retrieved_chunks": [
                {"doc_id": c.doc_id, "chunk_id": c.chunk_id, "score": round(s, 4), "text": c.text}
                for c, s in top_chunks
            ],
        }


def initialize_knowledge_base() -> OpenAIRAGEngine:
    engine = OpenAIRAGEngine()
    engine.ingest_document(
        "architecture_guide.txt",
        "The AI Engineering Hub uses modular architecture with RAG, autonomous agents, and production evals. "
        "Each course provides zero-dependency exercises and portfolio-ready capstone projects for learners."
    )
    engine.ingest_document(
        "deployment_manual.txt",
        "Deploying LLM apps requires rate limiting, exponential backoff retries, and fallback model chains. "
        "Always log latency metrics, token consumption, and cost per request to maintain budget guardrails."
    )
    return engine


def main():
    engine = initialize_knowledge_base()

    if "--serve" in sys.argv:
        try:
            import uvicorn
            from fastapi import FastAPI

            app = FastAPI(title="Doc Q&A Bot API")

            @app.get("/query")
            def query_endpoint(q: str):
                return engine.answer_query(q)

            print("Starting FastAPI server at http://127.0.0.1:8000 ...")
            uvicorn.run(app, host="127.0.0.1", port=8000)
        except ImportError:
            print("Error: FastAPI and Uvicorn required for web mode. Run: pip install fastapi uvicorn")
    else:
        print("=" * 60)
        print("  Document Q&A Bot (Real OpenAI RAG Starter CLI)")
        print("=" * 60)
        sample_query = "What is required for deploying LLM apps?"
        print(f"\nUser Query: {sample_query}\n")
        res = engine.answer_query(sample_query)
        print(f"Answer:\n{res['answer']}")


if __name__ == "__main__":
    main()
