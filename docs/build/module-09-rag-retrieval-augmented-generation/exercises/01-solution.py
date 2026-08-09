"""
Exercise 01: Build a Real RAG Pipeline (Solution)
==================================================
Course 06 — RAG: Retrieval Augmented Generation
"""

import os
import math
from typing import List, Tuple, Dict, Any
from openai import OpenAI

DOCUMENTS = [
    "RAG stands for Retrieval-Augmented Generation. It combines a retriever with a generator to produce grounded answers.",
    "Vector databases store dense embeddings and support fast nearest-neighbor similarity search. Popular options include Chroma, Pinecone, and pgvector.",
    "Chunking is the process of splitting documents into smaller pieces for retrieval. Common strategies include fixed-size, sentence-based, and recursive splitting.",
    "Cosine similarity measures the angle between two vectors. A score of 1.0 means identical direction; 0.0 means orthogonal.",
    "The embedding model converts text into dense numerical vectors. OpenAI's text-embedding-3-small produces 1536-dimensional vectors.",
    "Hybrid search combines keyword search (BM25) with dense vector search to improve recall. Reciprocal Rank Fusion (RRF) merges result lists.",
    "In production RAG, you should log retrieval scores, latency, and the number of chunks retrieved per query for observability.",
    "Reranking is a second-stage retrieval step that uses a cross-encoder to re-score retrieved chunks for better precision.",
]


class RealRAGPipeline:
    """Production RAG Pipeline utilizing live OpenAI API models."""

    def __init__(self, embedding_model: str = "text-embedding-3-small", llm_model: str = "gpt-4o-mini"):
        self.client = OpenAI()
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        self.document_embeddings: List[Tuple[str, List[float]]] = []

    def get_embedding(self, text: str) -> List[float]:
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding

    def index_documents(self, docs: List[str]) -> None:
        self.document_embeddings = []
        for doc in docs:
            emb = self.get_embedding(doc)
            self.document_embeddings.append((doc, emb))

    @staticmethod
    def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        dot = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0
        return dot / (norm_a * norm_b)

    def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        q_emb = self.get_embedding(query)
        results = []
        for doc_text, doc_emb in self.document_embeddings:
            score = self.cosine_similarity(q_emb, doc_emb)
            results.append((doc_text, score))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def generate_answer(self, query: str, top_k: int = 3) -> str:
        retrieved_chunks = self.retrieve(query, top_k=top_k)
        context = "\n".join(f"[{i+1}] {text}" for i, (text, _) in enumerate(retrieved_chunks))

        system_prompt = (
            "You are an expert AI assistant. Answer the user question using ONLY the provided context. "
            "Cite sources inline using [1], [2], etc."
        )
        user_message = f"Context:\n{context}\n\nQuestion: {query}"

        response = self.client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.0,
        )
        return response.choices[0].message.content


if __name__ == "__main__":
    print("--- Initializing Real RAG Pipeline ---")
    rag = RealRAGPipeline()
    rag.index_documents(DOCUMENTS)
    print(f"Indexed {len(rag.document_embeddings)} document chunks with real embeddings.\n")

    queries = [
        "What is RAG?",
        "Explain hybrid search and RRF",
    ]

    for q in queries:
        print(f"Query: {q}")
        answer = rag.generate_answer(q)
        print(f"Answer:\n{answer}\n{'='*60}\n")
