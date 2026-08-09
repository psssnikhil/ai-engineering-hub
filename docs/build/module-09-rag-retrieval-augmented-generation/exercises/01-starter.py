"""
Exercise 01: Build a Real RAG Pipeline (Starter)
=================================================
Course 06 — RAG: Retrieval Augmented Generation

Goal: Build a real RAG pipeline using OpenAI Embeddings and GPT-4o-mini.
      Retrieves relevant chunks via vector similarity and generates grounded answers.

Instructions:
  1. Complete the TODO sections below.
  2. Run: python 01-starter.py
  3. Compare your output with 01-solution.py

Requirements: pip install openai
"""

import os
import math
from typing import List, Tuple, Dict, Any
from openai import OpenAI


# ── Sample Knowledge Base ──────────────────────────────────────────────
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
        """
        TODO: Fetch embedding vector from OpenAI API.
        Use self.client.embeddings.create(model=self.embedding_model, input=text).
        Return the embedding list of floats.
        """
        pass  # Your code here

    def index_documents(self, docs: List[str]) -> None:
        """
        TODO: Index all input documents by embedding each one and storing (doc_text, vector).
        """
        pass  # Your code here

    @staticmethod
    def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        """
        TODO: Compute cosine similarity between two dense float vectors.
        """
        pass  # Your code here

    def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        TODO: Embed query, compute cosine similarity against indexed document embeddings,
        and return top_k (doc_text, similarity_score) tuples sorted descending.
        """
        pass  # Your code here

    def generate_answer(self, query: str, top_k: int = 3) -> str:
        """
        TODO: Complete the end-to-end RAG generation:
        1. Retrieve top_k relevant context chunks using self.retrieve().
        2. Format prompt with retrieved context.
        3. Call OpenAI ChatCompletion (self.client.chat.completions.create).
        4. Return LLM generated response string.
        """
        pass  # Your code here


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
