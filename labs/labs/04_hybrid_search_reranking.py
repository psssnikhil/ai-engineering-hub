"""
Lab 04: Hybrid Search & Reciprocal Rank Fusion (RRF)
===================================================
Course 06 & 10 — Vector Databases & Retrieval

Combines keyword search (BM25 style) with dense vector search (OpenAI Embeddings / Offline Fallback)
and merges rankings using Reciprocal Rank Fusion (RRF).

Requirements:
  pip install openai anthropic
  export OPENAI_API_KEY="sk-..." (optional; falls back to offline mock mode)
"""

import math
import os
import sys
import hashlib
from collections import Counter
from typing import List, Tuple, Dict


DOCUMENTS = [
    "Dense vector search finds semantic similarity but can miss exact keyword matches like product codes.",
    "BM25 keyword search scores term frequency and inverse document frequency for exact word matching.",
    "Reciprocal Rank Fusion (RRF) combines rank positions from keyword and vector searches: RRF(d) = sum(1 / (k + rank(d))).",
    "Cross-encoder rerankers re-score retrieved candidates to maximize precision in multi-stage search pipelines.",
]


class HybridSearchEngine:
    def __init__(self, rrf_k: float = 60.0):
        self.rrf_k = rrf_k
        self.docs = DOCUMENTS
        self.embeddings: List[List[float]] = []
        self._openai_client = None

    def _get_embedding(self, text: str) -> List[float]:
        if os.getenv("OPENAI_API_KEY"):
            if self._openai_client is None:
                from openai import OpenAI
                self._openai_client = OpenAI()
            res = self._openai_client.embeddings.create(
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

    def index(self) -> None:
        self.embeddings = []
        for text in self.docs:
            self.embeddings.append(self._get_embedding(text))

    def _keyword_search(self, query: str) -> List[Tuple[int, float]]:
        q_tokens = query.lower().split()
        scored = []
        for idx, doc in enumerate(self.docs):
            d_tokens = doc.lower().split()
            counts = Counter(d_tokens)
            score = sum(counts[t] for t in q_tokens)
            scored.append((idx, float(score)))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored

    def _dense_search(self, query: str) -> List[Tuple[int, float]]:
        q_vec = self._get_embedding(query)

        scored = []
        for idx, d_vec in enumerate(self.embeddings):
            dot = sum(a * b for a, b in zip(q_vec, d_vec))
            norm_q = math.sqrt(sum(a * a for a in q_vec))
            norm_d = math.sqrt(sum(b * b for b in d_vec))
            score = dot / (norm_q * norm_d) if norm_q > 0 and norm_d > 0 else 0.0
            scored.append((idx, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored

    def search_rrf(self, query: str, top_k: int = 2) -> List[Tuple[str, float]]:
        kw_ranks = self._keyword_search(query)
        dense_ranks = self._dense_search(query)

        rrf_scores: Dict[int, float] = {}

        for rank, (idx, _) in enumerate(kw_ranks):
            rrf_scores[idx] = rrf_scores.get(idx, 0.0) + (1.0 / (self.rrf_k + rank + 1))

        for rank, (idx, _) in enumerate(dense_ranks):
            rrf_scores[idx] = rrf_scores.get(idx, 0.0) + (1.0 / (self.rrf_k + rank + 1))

        final_ranking = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        return [(self.docs[idx], score) for idx, score in final_ranking[:top_k]]


if __name__ == "__main__":
    print("--- Lab 04: Running Hybrid Search & RRF ---")
    engine = HybridSearchEngine()
    engine.index()

    q = "BM25 vector search rank fusion"
    print(f"Query: {q}\n")
    results = engine.search_rrf(q, top_k=2)
    for text, score in results:
        print(f"[{score:.5f}] {text}")
