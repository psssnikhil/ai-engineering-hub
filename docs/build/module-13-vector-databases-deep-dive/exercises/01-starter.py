"""
Exercise 01: Build a Vector Database Engine from Scratch (Starter)
===================================================================
Course 10 — Vector Databases Deep Dive

Goal: Implement an in-memory vector database engine with dense vector indexing,
      cosine similarity calculation, k-NN search using a max-heap, and metadata filtering.

Instructions:
  1. Complete the TODO sections below.
  2. Run: python 01-starter.py
  3. Compare your output with 01-solution.py

Zero external dependencies required — standard library Python only.
"""

import heapq
import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class VectorRecord:
    """Represents a document/vector entry in the vector database."""
    id: str
    vector: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)
    text: str = ""


@dataclass
class SearchResult:
    """Represents a scored search result."""
    id: str
    score: float
    metadata: Dict[str, Any]
    text: str


class VectorDatabase:
    """In-memory Vector Database supporting exact k-NN search and metadata filtering."""

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.records: Dict[str, VectorRecord] = {}

    def insert(self, record: VectorRecord) -> None:
        """
        TODO: Insert a record into the database.
        Verify that the vector dimension matches self.dimension.
        Raise ValueError if dimensions do not match.
        """
        pass  # Your code here

    def get(self, record_id: str) -> Optional[VectorRecord]:
        """Retrieve a record by ID."""
        return self.records.get(record_id)

    @staticmethod
    def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        """
        TODO: Calculate cosine similarity between two dense vectors.
        Formula: dot(a, b) / (||a|| * ||b||)

        Return 0.0 if either vector has zero norm.
        """
        pass  # Your code here

    def search(
        self,
        query_vector: List[float],
        top_k: int = 3,
        filter_metadata: Optional[Dict[str, Any]] = None,
    ) -> List[SearchResult]:
        """
        TODO: Perform exact k-Nearest Neighbors search.

        1. Verify query_vector dimension.
        2. Iterate over all records in self.records.
        3. If filter_metadata is provided, skip records that don't match ALL filter key-values.
        4. Calculate cosine similarity between query_vector and record.vector.
        5. Maintain top_k highest scoring records using heapq or sorting.
        6. Return a list of SearchResult objects sorted by score DESCENDING.
        """
        pass  # Your code here


# ── Run ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    db = VectorDatabase(dimension=4)

    sample_records = [
        VectorRecord(
            id="doc-1",
            vector=[0.9, 0.1, 0.85, 0.7],
            metadata={"category": "tech", "year": 2024},
            text="Autonomous AI agents in enterprise cloud software.",
        ),
        VectorRecord(
            id="doc-2",
            vector=[0.1, 0.95, 0.2, 0.3],
            metadata={"category": "finance", "year": 2024},
            text="Quarterly earnings report and corporate dividend yield.",
        ),
        VectorRecord(
            id="doc-3",
            vector=[0.8, 0.2, 0.9, 0.4],
            metadata={"category": "tech", "year": 2023},
            text="Transformer models and self-attention mechanisms in PyTorch.",
        ),
        VectorRecord(
            id="doc-4",
            vector=[0.2, 0.85, 0.1, 0.6],
            metadata={"category": "finance", "year": 2023},
            text="Central bank interest rate hikes and bond market volatility.",
        ),
        VectorRecord(
            id="doc-5",
            vector=[0.75, 0.3, 0.8, 0.85],
            metadata={"category": "tech", "year": 2024},
            text="Kubernetes deployment of LLM inference microservices.",
        ),
    ]

    for rec in sample_records:
        db.insert(rec)

    print(f"Database populated with {len(db.records)} records.")

    query_ai = [0.85, 0.15, 0.9, 0.6]
    print("\n--- Search Query: 'AI & Cloud Infrastructure' (Top 3) ---")
    results = db.search(query_ai, top_k=3)
    if results:
        for r in results:
            print(f"[{r.score:.4f}] ({r.id}) {r.text}")
    else:
        print("TODO: Complete the search method to see results!")

    print("\n--- Search Query with Filter: category='tech', year=2024 (Top 2) ---")
    results_filtered = db.search(
        query_ai, top_k=2, filter_metadata={"category": "tech", "year": 2024}
    )
    if results_filtered:
        for r in results_filtered:
            print(f"[{r.score:.4f}] ({r.id}) [{r.metadata}] {r.text}")
    else:
        print("TODO: Complete the search method to see results!")
