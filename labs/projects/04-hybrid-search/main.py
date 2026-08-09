"""
Project 04: Production-Grade Hybrid Search & Reciprocal Rank Fusion (RRF)
========================================================================
Course 06 & 10 — Vector Databases & Retrieval

Features:
  1. Complete BM25 Engine: Handcrafted TF, IDF, document length scaling, and average length parameters.
  2. Text Preprocessing: Custom tokenization, stop-word removal, and basic English suffix stemming.
  3. Dense Retrieval: Custom cosine similarity calculations using normalized vector matching.
  4. Configurable RRF Merger: Blends rankings from sparse and dense vectors with custom rank bias factors.
"""

import math
import os
import sys
import hashlib
from collections import Counter
from typing import List, Tuple, Dict, Set

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from labs.common import load_sample_documents

# Standard stop words for filtering
STOP_WORDS: Set[str] = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "arent",
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by",
    "can", "cant", "cannot", "could", "did", "do", "does", "doing", "don", "down", "during", "each",
    "few", "for", "from", "further", "had", "has", "have", "having", "he", "her", "here", "hers",
    "herself", "him", "himself", "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself",
    "just", "me", "more", "most", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only",
    "or", "other", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "should", "so",
    "some", "such", "than", "that", "the", "their", "theirs", "them", "themselves", "then", "there",
    "these", "they", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was",
    "we", "were", "what", "when", "where", "which", "while", "who", "whom", "why", "with", "would",
    "you", "your", "yours", "yourself", "yourselves"
}


class TextPreprocessor:
    """Preprocesses search text: downcases, removes stop-words, and stems suffixes."""
    @staticmethod
    def tokenize(text: str) -> List[str]:
        # Simple word tokenization using regex
        import re
        words = re.findall(r'\b\w+\b', text.lower())
        return words

    @staticmethod
    def stem(word: str) -> str:
        """Naive English suffix stemmer for clean index reduction."""
        if len(word) <= 3:
            return word
        # Strip common suffixes
        suffixes = ["ing", "ly", "ment", "ed", "es", "s"]
        for suffix in suffixes:
            if word.endswith(suffix):
                return word[:-len(suffix)]
        return word

    @classmethod
    def preprocess(cls, text: str) -> List[str]:
        tokens = cls.tokenize(text)
        # Filter stop words and stem
        cleaned = [cls.stem(t) for t in tokens if t not in STOP_WORDS]
        return cleaned


class BM25Engine:
    """Production BM25 ranker implemented from scratch."""
    def __init__(self, docs: List[str], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.docs = docs
        self.N = len(docs)
        
        # Tokenize and index documents
        self.doc_tokens = [TextPreprocessor.preprocess(doc) for doc in docs]
        self.doc_lengths = [len(tokens) for tokens in self.doc_tokens]
        self.avg_doc_len = sum(self.doc_lengths) / self.N if self.N > 0 else 1.0
        
        # Calculate Term Frequencies (TF) and Document Frequencies (DF)
        self.doc_tfs: List[Counter] = [Counter(tokens) for tokens in self.doc_tokens]
        self.df: Dict[str, int] = {}
        for tokens in self.doc_tokens:
            unique_tokens = set(tokens)
            for token in unique_tokens:
                self.df[token] = self.df.get(token, 0) + 1

    def idf(self, term: str) -> float:
        df_t = self.df.get(term, 0)
        # Standard BM25 IDF formulation with smoothing
        numerator = self.N - df_t + 0.5
        denominator = df_t + 0.5
        return math.log(max(1.0001, (numerator / denominator) + 1.0))

    def score(self, query: str) -> List[Tuple[int, float]]:
        q_tokens = TextPreprocessor.preprocess(query)
        scored_docs = []

        for idx in range(self.N):
            doc_len = self.doc_lengths[idx]
            tf_map = self.doc_tfs[idx]
            doc_score = 0.0

            for token in q_tokens:
                if token not in self.df:
                    continue
                tf = tf_map[token]
                idf = self.idf(token)
                
                # BM25 scoring formulation
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * (doc_len / self.avg_doc_len))
                doc_score += idf * (numerator / denominator)

            scored_docs.append((idx, doc_score))

        # Sort descending by BM25 score
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        return scored_docs


class DenseEngine:
    """Vector database simulation handling dense search queries."""
    def __init__(self, docs: List[str]):
        self.docs = docs
        self.embeddings: List[List[float]] = []
        self._openai_client = None

    def _get_embedding(self, text: str) -> List[float]:
        if os.getenv("OPENAI_API_KEY"):
            if self._openai_client is None:
                from openai import OpenAI
                self._openai_client = OpenAI()
            try:
                res = self._openai_client.embeddings.create(
                    model="text-embedding-3-small",
                    input=text
                )
                return res.data[0].embedding
            except Exception as e:
                print(f"[Warning] Dense embedding API failed: {e}. Using fallback.")
                return self._offline_embedding(text)
        else:
            return self._offline_embedding(text)

    def _offline_embedding(self, text: str) -> List[float]:
        """Deterministic unit vector generation for keyless runs."""
        words = text.lower().split()
        vec = [0.0] * 64
        for w in words:
            h = hashlib.md5(w.encode()).hexdigest()
            idx = int(h, 16) % 64
            vec[idx] += 1.0
        
        # Normalize unit length
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [x / norm for x in vec]
        return vec

    def index(self) -> None:
        self.embeddings = [self._get_embedding(doc) for doc in self.docs]

    @staticmethod
    def _cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        dot = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        return dot / (norm_a * norm_b) if norm_a > 0 and norm_b > 0 else 0.0

    def score(self, query: str) -> List[Tuple[int, float]]:
        q_vec = self._get_embedding(query)
        scored = []
        for idx, d_vec in enumerate(self.embeddings):
            sim = self._cosine_similarity(q_vec, d_vec)
            scored.append((idx, sim))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored


class HybridSearchEngine:
    def __init__(self, rrf_k: float = 60.0):
        self.rrf_k = rrf_k
        self.docs = load_sample_documents()
        self.sparse_engine = BM25Engine(self.docs)
        self.dense_engine = DenseEngine(self.docs)

    def index(self) -> None:
        # Precompute dense embeddings
        self.dense_engine.index()

    def search_rrf(self, query: str, top_k: int = 3, lexical_weight: float = 1.0, dense_weight: float = 1.0) -> List[Tuple[str, float]]:
        # 1. Get raw search scores & rankings
        lexical_ranks = self.sparse_engine.score(query)
        dense_ranks = self.dense_engine.score(query)

        # 2. Map docs to RRF scores
        rrf_scores: Dict[int, float] = {}

        # Add lexical rank scores
        for rank, (idx, _) in enumerate(lexical_ranks):
            rrf_scores[idx] = rrf_scores.get(idx, 0.0) + lexical_weight * (1.0 / (self.rrf_k + rank + 1))

        # Add dense rank scores
        for rank, (idx, _) in enumerate(dense_ranks):
            rrf_scores[idx] = rrf_scores.get(idx, 0.0) + dense_weight * (1.0 / (self.rrf_k + rank + 1))

        # 3. Sort by aggregated RRF score
        sorted_results = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        
        return [(self.docs[idx], score) for idx, score in sorted_results[:top_k]]


if __name__ == "__main__":
    print("=== Running Production Hybrid Search (BM25 + Dense RRF) ===")
    engine = HybridSearchEngine()
    engine.index()

    query = "Evaluating agents and executing actions safely using tools."
    print(f"Query: {query}\n")

    results = engine.search_rrf(query, top_k=3, lexical_weight=1.0, dense_weight=1.2)
    print("Top retrieved documents (RRF blended):")
    for doc, score in results:
        print(f"  [{score:.6f}] {doc[:100]}...")
