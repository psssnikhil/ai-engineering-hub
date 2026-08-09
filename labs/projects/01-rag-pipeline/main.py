"""
Project 01: Production-Grade RAG Pipeline from Scratch
======================================================
Course 06 — RAG: Retrieval Augmented Generation

Features:
  1. LRU Cache for Embeddings: Prevents redundant API calls.
  2. Advanced Splitters:
     - Recursive Character Text Chunker (respects paragraph/sentence boundaries).
     - Semantic Chunker (splits by sentence, groups based on similarity distance).
  3. Query Expansion & Preprocessing (synonyms/alternative query formulation via LLM).
  4. Self-Corrective RAG (LLM Judge checks chunk relevance before generating the answer).
  5. Multi-provider gateway integration with keyless offline fallback.
"""

import math
import os
import sys
import hashlib
import re
from dataclasses import dataclass
from typing import List, Tuple, Dict, Any, Optional

# Ensure repository root is on sys.path for labs.common imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from labs.common import LLMGateway, load_sample_documents

# In-Memory LRU Cache for Embeddings
EMBEDDING_CACHE: Dict[str, List[float]] = {}
CACHE_LIMIT = 500


@dataclass
class Chunk:
    id: str
    doc_id: int
    text: str
    vector: List[float]
    metadata: Dict[str, Any]


class EmbeddingEngine:
    """Handles embedding generation with local caching and offline fallback."""
    def __init__(self):
        self._openai_client = None

    def _get_openai_client(self):
        if self._openai_client is None and os.getenv("OPENAI_API_KEY"):
            from openai import OpenAI
            self._openai_client = OpenAI()
        return self._openai_client

    def get_embedding(self, text: str) -> List[float]:
        # Normalize text
        normalized_text = " ".join(text.split()).lower()
        
        # Check cache
        if normalized_text in EMBEDDING_CACHE:
            return EMBEDDING_CACHE[normalized_text]

        client = self._get_openai_client()
        if client:
            try:
                res = client.embeddings.create(
                    model="text-embedding-3-small",
                    input=normalized_text
                )
                vec = res.data[0].embedding
            except Exception as e:
                print(f"[Warning] Embedding API call failed: {e}. Falling back to offline pseudo-embedding.")
                vec = self._generate_pseudo_embedding(normalized_text)
        else:
            vec = self._generate_pseudo_embedding(normalized_text)

        # Enforce LRU cache eviction
        if len(EMBEDDING_CACHE) >= CACHE_LIMIT:
            # Evict first key
            first_key = next(iter(EMBEDDING_CACHE))
            del EMBEDDING_CACHE[first_key]
        
        EMBEDDING_CACHE[normalized_text] = vec
        return vec

    def _generate_pseudo_embedding(self, text: str) -> List[float]:
        """Deterministic pseudo-embedding for offline execution."""
        words = text.split()
        vec = [0.05] * 64  # Small base bias
        for w in words:
            # Generate deterministic index and values
            h = hashlib.md5(w.encode("utf-8")).hexdigest()
            idx = int(h[:4], 16) % 64
            val = (int(h[4:8], 16) % 100) / 100.0
            vec[idx] += val
            
        # Normalize vector to unit length
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [x / norm for x in vec]
        return vec


class RecursiveCharacterChunker:
    """Splits text into chunks using a hierarchical list of separators."""
    def __init__(self, chunk_size: int = 200, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = ["\n\n", "\n", " ", ""]

    def split(self, text: str) -> List[str]:
        return self._split_text(text, self.separators)

    def _split_text(self, text: str, separators: List[str]) -> List[str]:
        final_chunks = []
        if len(text) <= self.chunk_size:
            return [text]

        # Select separator
        separator = separators[-1]
        for s in separators:
            if s == "":
                separator = s
                break
            if s in text:
                separator = s
                break

        # Split text
        if separator != "":
            splits = text.split(separator)
        else:
            splits = list(text)

        current_doc = []
        current_len = 0

        for part in splits:
            part_len = len(part)
            # If a single part exceeds chunk size, recursively split it with remaining separators
            if part_len > self.chunk_size:
                if current_doc:
                    final_chunks.append(separator.join(current_doc))
                    current_doc = []
                    current_len = 0
                remaining_seps = [s for s in separators if s != separator]
                final_chunks.extend(self._split_text(part, remaining_seps))
            elif current_len + part_len + (len(separator) if current_doc else 0) <= self.chunk_size:
                current_doc.append(part)
                current_len += part_len + (len(separator) if len(current_doc) > 1 else 0)
            else:
                if current_doc:
                    final_chunks.append(separator.join(current_doc))
                # Form overlapping start
                overlap_doc = []
                overlap_len = 0
                for prev in reversed(current_doc):
                    if overlap_len + len(prev) + (len(separator) if overlap_doc else 0) <= self.chunk_overlap:
                        overlap_doc.insert(0, prev)
                        overlap_len += len(prev) + (len(separator) if len(overlap_doc) > 1 else 0)
                    else:
                        break
                current_doc = overlap_doc + [part]
                current_len = sum(len(x) for x in current_doc) + (len(separator) * (len(current_doc) - 1))

        if current_doc:
            final_chunks.append(separator.join(current_doc))

        return [c.strip() for c in final_chunks if c.strip()]


class SemanticChunker:
    """Groups sentences together based on similarity of their embeddings."""
    def __init__(self, embedding_engine: EmbeddingEngine, similarity_threshold: float = 0.82):
        self.engine = embedding_engine
        self.threshold = similarity_threshold

    def split(self, text: str) -> List[str]:
        # Split into sentences using a regex
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        sentences = [s.strip() for s in sentences if s.strip()]
        if not sentences:
            return []

        # Get embeddings
        embeddings = [self.engine.get_embedding(s) for s in sentences]
        
        chunks = []
        current_chunk = [sentences[0]]
        
        for i in range(1, len(sentences)):
            sim = self._cosine_similarity(embeddings[i-1], embeddings[i])
            if sim >= self.threshold:
                current_chunk.append(sentences[i])
            else:
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentences[i]]
                
        if current_chunk:
            chunks.append(" ".join(current_chunk))
            
        return chunks

    def _cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        dot = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        return dot / (norm_a * norm_b) if norm_a > 0 and norm_b > 0 else 0.0


class ProductionRAGPipeline:
    def __init__(self, gateway: Optional[LLMGateway] = None, chunking_strategy: str = "recursive"):
        self.gateway = gateway or LLMGateway()
        self.emb_engine = EmbeddingEngine()
        self.chunks: List[Chunk] = []
        self.chunking_strategy = chunking_strategy

    def index(self, docs: List[str]) -> None:
        self.chunks = []
        chunk_idx = 1
        
        for doc_id, doc in enumerate(docs, start=1):
            if self.chunking_strategy == "semantic":
                chunker = SemanticChunker(self.emb_engine)
                text_chunks = chunker.split(doc)
            else:
                chunker = RecursiveCharacterChunker(chunk_size=150, chunk_overlap=30)
                text_chunks = chunker.split(doc)

            for chunk_text in text_chunks:
                vec = self.emb_engine.get_embedding(chunk_text)
                self.chunks.append(Chunk(
                    id=f"doc_{doc_id}_chunk_{chunk_idx}",
                    doc_id=doc_id,
                    text=chunk_text,
                    vector=vec,
                    metadata={"doc_id": doc_id, "length": len(chunk_text)}
                ))
                chunk_idx += 1
        print(f"[RAG Index] Built {len(self.chunks)} chunks using strategy '{self.chunking_strategy}'.")

    @staticmethod
    def _cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        dot = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        return dot / (norm_a * norm_b) if norm_a > 0 and norm_b > 0 else 0.0

    def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[Chunk, float]]:
        q_vec = self.emb_engine.get_embedding(query)
        scored = []
        for c in self.chunks:
            score = self._cosine_similarity(q_vec, c.vector)
            scored.append((c, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def expand_query(self, original_query: str) -> List[str]:
        """Generate alternative search terms using LLM for broader coverage."""
        prompt = (
            f"Generate exactly 2 alternative search queries/synonyms for: '{original_query}'. "
            "Return them as a flat comma-separated list. No numbering, no introduction."
        )
        try:
            resp = self.gateway.generate(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            queries = [q.strip().strip('"').strip("'") for q in resp.content.split(",")]
            # Filter empty or redundant
            valid_queries = [original_query]
            for q in queries:
                if q and q.lower() != original_query.lower() and len(q) > 3:
                    valid_queries.append(q)
            return valid_queries[:3]
        except Exception:
            # Fallback to single original query
            return [original_query]

    def execute_hybrid_retrieval(self, query: str, top_k: int = 3) -> List[Chunk]:
        """Expands query, fetches chunks for all terms, dedupes them, and keeps best candidates."""
        expanded_queries = self.expand_query(query)
        print(f"  [RAG Query Expansion] Queries: {expanded_queries}")

        candidate_map: Dict[str, Tuple[Chunk, float]] = {}
        for q in expanded_queries:
            results = self.retrieve(q, top_k=top_k)
            for chunk, score in results:
                # Keep highest score if chunk retrieved multiple times
                if chunk.id not in candidate_map or score > candidate_map[chunk.id][1]:
                    candidate_map[chunk.id] = (chunk, score)
        
        # Sort and take top_k
        sorted_candidates = sorted(candidate_map.values(), key=lambda x: x[1], reverse=True)
        return [c[0] for c in sorted_candidates[:top_k]]

    def evaluate_and_filter_chunks(self, query: str, chunks: List[Chunk]) -> List[Chunk]:
        """Self-Corrective step: evaluate retrieved chunks for relevance to query."""
        relevant_chunks = []
        for c in chunks:
            # Use light heuristic first: keyword intersection
            q_words = set(re.findall(r'\w+', query.lower()))
            c_words = set(re.findall(r'\w+', c.text.lower()))
            common = q_words.intersection(c_words)
            
            # If intersection has elements, or if we evaluate via LLM Judge
            if len(common) >= 1:
                relevant_chunks.append(c)
            else:
                # LLM Judge verification for tricky semantic matches
                judge_prompt = (
                    f"Task: Assess if the context snippet is relevant to answering the query.\n"
                    f"Query: {query}\n"
                    f"Snippet: {c.text}\n"
                    f"Reply with 'YES' if it has any helpful info, otherwise 'NO'."
                )
                try:
                    resp = self.gateway.generate(
                        messages=[{"role": "user", "content": judge_prompt}],
                        temperature=0.0
                    )
                    if "YES" in resp.content.upper():
                        relevant_chunks.append(c)
                except Exception:
                    # Fallback to keep chunk if LLM call fails
                    relevant_chunks.append(c)
        return relevant_chunks

    def query(self, user_query: str) -> str:
        # Step 1: Hybrid / Expanded Retrieval
        retrieved = self.execute_hybrid_retrieval(user_query, top_k=3)
        
        # Step 2: Self-Corrective Relevance Check
        filtered = self.evaluate_and_filter_chunks(user_query, retrieved)
        print(f"  [RAG Self-Correction] Kept {len(filtered)} / {len(retrieved)} retrieved chunks.")

        if not filtered:
            return "I could not find any relevant information in the provided context to answer your question."

        context = "\n".join(f"[Doc {c.metadata['doc_id']}] {c.text}" for c in filtered)

        messages = [
            {
                "role": "system", 
                "content": (
                    "You are a precise production assistant. Answer the user query based ONLY on the provided context. "
                    "If the context is insufficient, explain what is missing. Cite sources using [Doc ID]."
                )
            },
            {"role": "user", "content": f"Context:\n{context}\n\nQuery: {user_query}"}
        ]

        response = self.gateway.generate(messages=messages, temperature=0.0)
        return response.content


if __name__ == "__main__":
    print("--- Running Production-Grade RAG Pipeline ---")
    DOCUMENTS = load_sample_documents()
    
    # Run with semantic chunking first
    pipeline = ProductionRAGPipeline(chunking_strategy="semantic")
    pipeline.index(DOCUMENTS)

    q = "Explain what ReAct agents do and how they run."
    print(f"\nQuery: {q}")
    ans = pipeline.query(q)
    print(f"Answer:\n{ans}\n")
    
    # Verify LRU cache is working
    print(f"Cached Embedding Items count: {len(EMBEDDING_CACHE)}")
