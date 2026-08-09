"""
Sample dataset loader utility for AI Engineering Hub labs.
"""

import os
from typing import List, Dict

DOCUMENTS_PATH = os.path.join(os.path.dirname(__file__), "documents.md")


def load_sample_documents() -> List[str]:
    """
    Load sections from labs/common/documents.md as a list of document strings.
    """
    if not os.path.exists(DOCUMENTS_PATH):
        return [
            "RAG combines retrieval with LLM text generation.",
            "ReAct agents use thought, action, and observation steps.",
            "Vector databases store high-dimensional embeddings."
        ]

    with open(DOCUMENTS_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by section headers (## Document X:)
    raw_sections = content.split("## Document ")
    documents = []
    for sec in raw_sections[1:]:  # skip preamble
        lines = sec.strip().split("\n")
        # Keep text body excluding header line
        body = "\n".join(lines[1:]).strip()
        if body:
            documents.append(body)

    return documents
