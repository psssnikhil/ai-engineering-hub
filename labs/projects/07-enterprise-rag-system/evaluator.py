"""
Enterprise RAG System Quality Evaluator.
========================================
Performs automated LLM-as-a-Judge evaluations on RAG responses:
  1. Faithfulness Score (no hallucinations, grounded in context).
  2. Answer Relevance Score (answers the prompt directly).
  3. JSON structure recovery and score threshold evaluation.
"""

import json
import re
from typing import Dict, Any, Optional
from labs.common.gateway import LLMGateway


class QualityEvaluator:
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()

    def evaluate_groundedness(self, query: str, context: str, answer: str) -> Dict[str, Any]:
        system_prompt = (
            "You are an expert AI Quality Judge. Score the provided response for groundedness "
            "(faithfulness to context) and relevance (addressing query) on a scale of 0.0 to 1.0.\n\n"
            "Return EXACTLY this JSON structure, with no markdown wrappers:\n"
            "{\n"
            "  \"faithfulness\": <float>,\n"
            "  \"relevance\": <float>,\n"
            "  \"explanation\": \"<short reason for score>\"\n"
            "}"
        )
        user_msg = f"Query: {query}\n\nContext:\n{context}\n\nResponse:\n{answer}"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg},
        ]

        try:
            resp = self.gateway.generate(messages=messages, temperature=0.0)
            cleaned = resp.content.strip()
            
            # Clean markdown code blocks if present
            if cleaned.startswith("```"):
                match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, re.DOTALL)
                if match:
                    cleaned = match.group(1)
            
            parsed = json.loads(cleaned)
            return {
                "faithfulness": min(1.0, max(0.0, float(parsed.get("faithfulness", 0.0)))),
                "relevance": min(1.0, max(0.0, float(parsed.get("relevance", 0.0)))),
                "explanation": parsed.get("explanation", "Parsed successfully.")
            }
        except Exception as e:
            # Safe offline fallback scores based on simple heuristic overlap
            print(f"    [Evaluator Warning] LLM Judge call or parsing failed: {e}. Running local keyword overlap fallback.")
            q_words = set(query.lower().split())
            a_words = set(answer.lower().split())
            c_words = set(context.lower().split())
            
            faith = len(a_words.intersection(c_words)) / max(1, len(a_words))
            rel = len(a_words.intersection(q_words)) / max(1, len(q_words))
            
            return {
                "faithfulness": round(min(1.0, faith + 0.5), 2),  # add smoothing bias
                "relevance": round(min(1.0, rel + 0.4), 2),
                "explanation": f"Local heuristic fallback due to judge exception: {e}"
            }
