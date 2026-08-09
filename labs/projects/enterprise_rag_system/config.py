"""Configuration settings for Enterprise RAG System."""

import os

EMBEDDING_MODEL = "text-embedding-3-small"
PRIMARY_LLM_MODEL = "gpt-4o-mini"
FALLBACK_LLM_MODEL = "claude-3-5-haiku-20241022"

DEFAULT_TOP_K = 3
CHUNK_SIZE_WORDS = 40
MIN_FAITHFULNESS_THRESHOLD = 0.60
