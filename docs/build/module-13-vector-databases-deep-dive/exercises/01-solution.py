"""
Exercise 01: Build a Vector Database Engine from Scratch (Solution)
====================================================================
Course 10 — Vector Databases Deep Dive
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
        """Insert a record into the database with dimension validation."""
        if len(record.vector) != self.dimension:
            raise ValueError(
                f"Dimension mismatch: expected {self.dimension}, got {len(record.vector)}"
            )
        self.records[record.id] = record

    def get(self, record_id: str) -> Optional[VectorRecord]:
        """Retrieve a record by ID."""
        return self.records.get(record_id)

    @staticmethod
    def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        """Calculate cosine similarity between two dense vectors: dot(a, b) / (||a|| * ||b||)."""
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))

        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0

        return dot_product / (norm_a * norm_b)

    def search(
        self,
        query_vector: List[float],
        top_k: int = 3,
        filter_metadata: Optional[Dict[str, Any]] = None,
    ) -> List[SearchResult]:
        """Perform exact k-NN search with metadata filtering."""
        if len(query_vector) != self.dimension:
            raise ValueError(
                f"Query dimension mismatch: expected {self.dimension}, got {len(query_vector)}"
            )

        candidates: List[SearchResult] = []

        for record in self.records.values():
            # Check metadata filter matching
            if filter_metadata:
                match = True
                for k, v in filter_metadata.items():
                    if record.metadata.get(k) != v:
                        match = False
                        break
                if not match:
                    continue

            score = self.cosine_similarity(query_vector, record.vector)
            candidates.append(
                SearchResult(
                    id=record.id,
                    score=score,
                    metadata=record.metadata,
                    text=record.text,
                )
            )

        # Sort descending by score
        candidates.sort(key=lambda x: x.score, reverse=True)
        return candidates[:top_k]


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
    for r in results:
        print(f"[{r.score:.4f}] ({r.id}) {r.text}")

    print("\n--- Search Query with Filter: category='tech', year=2024 (Top 2) ---")
    results_filtered = db.search(
        query_ai, top_k=2, filter_metadata={"category": "tech", "year": 2024}
    )
    for r in results_filtered:
        print(f"[{r.score:.4f}] ({r.id}) [{r.metadata}] {r.text}")
