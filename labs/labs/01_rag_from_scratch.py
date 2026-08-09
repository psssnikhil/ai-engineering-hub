"""
Lab 01: RAG Pipeline from Scratch
=================================
Course 06 — RAG: Retrieval Augmented Generation

A pure, modular Python implementation of a RAG pipeline without framework bloat.
Demonstrates document chunking, dense vector retrieval via OpenAI embeddings (with offline fallback),
and grounded answer generation via LLMGateway.

Requirements:
  pip install openai anthropic
  export OPENAI_API_KEY="sk-..." (optional; falls back to offline mock mode)
"""

import math
import os
import sys
import hashlib
from dataclasses import dataclass
from typing import List, Tuple, Dict, Any, Optional

# Ensure repository root is on sys.path for labs.common imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from labs.common.gateway import LLMGateway


DOCUMENTS = [
    "RAG stands for Retrieval-Augmented Generation. It combines a retriever with a generator to produce grounded answers.",
    "Vector databases store dense embeddings and support fast nearest-neighbor similarity search. Popular options include Chroma, Pinecone, and pgvector.",
    "Chunking is the process of splitting documents into smaller pieces for retrieval. Common strategies include fixed-size, sentence-based, and recursive splitting.",
    "Cosine similarity measures the angle between two vectors. A score of 1.0 means identical direction; 0.0 means orthogonal.",
    "The embedding model converts text into dense numerical vectors. OpenAI's text-embedding-3-small produces 1536-dimensional vectors.",
    "Hybrid search combines keyword search (BM25) with dense vector search to improve recall. Reciprocal Rank Fusion (RRF) merges result lists.",
]


@dataclass
class Chunk:
    id: int
    text: str
    vector: List[float]


class RAGPipeline:
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()
        self.chunks: List[Chunk] = []
        self._openai_client = None

    def _get_openai_client(self):
        if self._openai_client is None and os.getenv("OPENAI_API_KEY"):
            from openai import OpenAI
            self._openai_client = OpenAI()
        return self._openai_client

    def get_embedding(self, text: str) -> List[float]:
        client = self._get_openai_client()
        if client:
            res = client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return res.data[0].embedding
        else:
            # Deterministic pseudo-embedding for offline keyless execution
            words = text.lower().split()
            vec = [0.0] * 64
            for w in words:
                idx = int(hashlib.md5(w.encode()).hexdigest(), 16) % 64
                vec[idx] += 1.0
            return vec

    def index(self, docs: List[str]) -> None:
        self.chunks = []
        for i, text in enumerate(docs):
            vec = self.get_embedding(text)
            self.chunks.append(Chunk(id=i + 1, text=text, vector=vec))

    @staticmethod
    def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        dot = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        return dot / (norm_a * norm_b) if norm_a > 0 and norm_b > 0 else 0.0

    def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[Chunk, float]]:
        q_vec = self.get_embedding(query)
        scored = []
        for c in self.chunks:
            score = self.cosine_similarity(q_vec, c.vector)
            scored.append((c, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def query(self, user_query: str) -> str:
        results = self.retrieve(user_query, top_k=3)
        context = "\n".join(f"[{c.id}] {c.text}" for c, _ in results)

        messages = [
            {"role": "system", "content": "Answer the question based ONLY on the context provided. Cite sources inline using [1], [2]."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_query}"}
        ]

        response = self.gateway.generate(messages=messages, temperature=0.0)
        return response.content


if __name__ == "__main__":
    print("--- Lab 01: Running RAG Pipeline ---")
    pipeline = RAGPipeline()
    pipeline.index(DOCUMENTS)

    q = "What is RAG and how does it work?"
    print(f"Query: {q}")
    ans = pipeline.query(q)
    print(f"Answer:\n{ans}")
