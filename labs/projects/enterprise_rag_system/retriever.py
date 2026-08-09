"""Dense Vector & Hybrid Retriever Module."""

import math
from dataclasses import dataclass
from typing import List, Tuple
from openai import OpenAI
from .config import EMBEDDING_MODEL, CHUNK_SIZE_WORDS


@dataclass
class DocumentChunk:
    doc_id: str
    chunk_id: int
    text: str
    vector: List[float]


class DenseRetriever:
    def __init__(self):
        self.client = OpenAI()
        self.chunks: List[DocumentChunk] = []

    def _embed(self, text: str) -> List[float]:
        res = self.client.embeddings.create(model=EMBEDDING_MODEL, input=text)
        return res.data[0].embedding

    def ingest(self, doc_id: str, content: str) -> None:
        words = content.split()
        chunk_idx = 1
        for i in range(0, len(words), CHUNK_SIZE_WORDS):
            chunk_text = " ".join(words[i:i + CHUNK_SIZE_WORDS])
            vector = self._embed(chunk_text)
            self.chunks.append(DocumentChunk(doc_id=doc_id, chunk_id=chunk_idx, text=chunk_text, vector=vector))
            chunk_idx += 1

    @staticmethod
    def _cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        dot = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        return dot / (norm_a * norm_b) if norm_a > 0 and norm_b > 0 else 0.0

    def search(self, query: str, top_k: int = 3) -> List[Tuple[DocumentChunk, float]]:
        q_vec = self._embed(query)
        results = []
        for chunk in self.chunks:
            score = self._cosine_similarity(q_vec, chunk.vector)
            results.append((chunk, score))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
