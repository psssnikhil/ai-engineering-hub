"""Automated LLM-as-a-Judge Evaluation Module."""

import json
from typing import Dict, Any, Optional
from labs.common.gateway import LLMGateway, OpenAIProvider


class QualityEvaluator:
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway([OpenAIProvider()])

    def evaluate_groundedness(self, query: str, context: str, answer: str) -> Dict[str, Any]:
        system_prompt = (
            "You are an AI Quality Judge. Score response groundedness and relevance (0.0 to 1.0). "
            "Return JSON: {\"faithfulness\": float, \"relevance\": float, \"explanation\": string}"
        )
        user_msg = f"Query: {query}\nContext: {context}\nAnswer: {answer}"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg},
        ]

        resp = self.gateway.generate(messages=messages, temperature=0.0)
        try:
            return json.loads(resp.content)
        except Exception:
            return {"faithfulness": 0.0, "relevance": 0.0, "explanation": "JSON Parse Error"}
