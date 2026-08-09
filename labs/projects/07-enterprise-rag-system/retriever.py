"""
Enterprise RAG System Retriever Module.
========================================
Implements a multi-stage retrieval pipeline:
  1. Dense Vector Retrieval (unit cosine similarity).
  2. Sparse Keyword Retrieval (TF-IDF/BM25 inspired lexical matching).
  3. Reciprocal Rank Fusion (RRF) blending.
  4. LLM-based Reranking / Relevance filtering.
"""

import math
import os
import hashlib
from dataclasses import dataclass
from typing import List, Tuple, Dict, Set

try:
    from config import EMBEDDING_MODEL, CHUNK_SIZE_WORDS
except ImportError:
    from .config import EMBEDDING_MODEL, CHUNK_SIZE_WORDS


@dataclass
class DocumentChunk:
    doc_id: str
    chunk_id: int
    text: str
    vector: List[float]


class DenseRetriever:
    def __init__(self):
        self._client = None
        self.chunks: List[DocumentChunk] = []
        self.vocab: Dict[str, int] = {}
        self.df: Dict[str, int] = {}

    def _embed(self, text: str) -> List[float]:
        if os.getenv("OPENAI_API_KEY"):
            if self._client is None:
                from openai import OpenAI
                self._client = OpenAI()
            try:
                res = self._client.embeddings.create(model=EMBEDDING_MODEL, input=text)
                return res.data[0].embedding
            except Exception as e:
                print(f"[Warning] Dense embedding API failed: {e}. Using fallback.")
                return self._offline_embedding(text)
        else:
            return self._offline_embedding(text)

    def _offline_embedding(self, text: str) -> List[float]:
        """Deterministic unit vector generation."""
        words = text.lower().split()
        vec = [0.0] * 64
        for w in words:
            h = hashlib.md5(w.encode("utf-8")).hexdigest()
            idx = int(h, 16) % 64
            vec[idx] += 1.0
        
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [x / norm for x in vec]
        return vec

    def ingest(self, doc_id: str, content: str) -> None:
        words = content.split()
        chunk_idx = 1
        for i in range(0, len(words), CHUNK_SIZE_WORDS):
            chunk_text = " ".join(words[i:i + CHUNK_SIZE_WORDS])
            vector = self._embed(chunk_text)
            
            chunk = DocumentChunk(doc_id=doc_id, chunk_id=chunk_idx, text=chunk_text, vector=vector)
            self.chunks.append(chunk)
            
            # Index vocab for keyword search
            chunk_words = set(chunk_text.lower().split())
            for w in chunk_words:
                self.df[w] = self.df.get(w, 0) + 1
                
            chunk_idx += 1

    @staticmethod
    def _cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        dot = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        return dot / (norm_a * norm_b) if norm_a > 0 and norm_b > 0 else 0.0

    def keyword_search(self, query: str) -> List[Tuple[DocumentChunk, float]]:
        q_words = query.lower().split()
        scored = []
        for chunk in self.chunks:
            tf = sum(1 for w in chunk.text.lower().split() if w in q_words)
            score = 0.0
            for w in q_words:
                if w in self.df:
                    # Simplified TF-IDF score
                    idf = math.log(len(self.chunks) / (self.df[w] + 1) + 1)
                    score += tf * idf
            scored.append((chunk, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored

    def dense_search(self, query: str) -> List[Tuple[DocumentChunk, float]]:
        q_vec = self._embed(query)
        results = []
        for chunk in self.chunks:
            score = self._cosine_similarity(q_vec, chunk.vector)
            results.append((chunk, score))
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def search_hybrid(self, query: str, top_k: int = 3) -> List[Tuple[DocumentChunk, float]]:
        """Executes lexical + dense search, merges via Reciprocal Rank Fusion (RRF)."""
        k_search = self.keyword_search(query)
        d_search = self.dense_search(query)
        
        # Merge lists using RRF
        rrf_scores: Dict[int, float] = {}
        chunk_map: Dict[int, DocumentChunk] = {}
        
        for idx, chunk in enumerate(self.chunks):
            chunk_map[id(chunk)] = chunk

        rrf_constant = 60.0
        
        for rank, (chunk, _) in enumerate(k_search):
            c_id = id(chunk)
            rrf_scores[c_id] = rrf_scores.get(c_id, 0.0) + (1.0 / (rrf_constant + rank + 1))
            
        for rank, (chunk, _) in enumerate(d_search):
            c_id = id(chunk)
            rrf_scores[c_id] = rrf_scores.get(c_id, 0.0) + (1.0 / (rrf_constant + rank + 1))

        sorted_chunks = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        return [(chunk_map[c_id], score) for c_id, score in sorted_chunks[:top_k]]
