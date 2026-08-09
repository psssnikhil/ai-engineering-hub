"""
AI Quality Evaluation Suite (Project #9 Starter)
================================================
Build These Project #9 — AI Engineering Hub

Features:
  - Golden dataset management
  - Real OpenAI LLM-as-a-Judge Rubric Evaluation (Faithfulness, Relevance, Conciseness)
  - Automated CI Quality Gate with pass/fail exit code
"""

import sys
import json
from dataclasses import dataclass
from typing import List, Dict, Any
from openai import OpenAI


@dataclass
class EvalTestCase:
    id: str
    prompt: str
    reference_context: str
    expected_answer: str


class OpenAIQualityJudge:
    """Production LLM-as-a-Judge using OpenAI API with structured JSON outputs."""

    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model

    def evaluate(self, prompt: str, context: str, actual_output: str) -> Dict[str, Any]:
        system_prompt = (
            "You are an impartial AI Quality Judge. Evaluate the assistant response against "
            "the user prompt and reference context. Return JSON with numeric scores (0.0 to 1.0) for:\n"
            "- faithfulness: Is the answer fully grounded in the context without hallucination?\n"
            "- relevance: Does the answer directly address the user's prompt?\n"
            "- conciseness: Is the answer succinct and free of filler fluff?\n"
            "- explanation: Brief sentence explaining the scores."
        )

        user_message = (
            f"User Prompt: {prompt}\n"
            f"Reference Context: {context}\n"
            f"Assistant Output: {actual_output}\n"
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            response_format={"type": "json_object"},
            temperature=0.0,
        )

        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {"faithfulness": 0.0, "relevance": 0.0, "conciseness": 0.0, "explanation": "JSON parse error"}


class QualityEvalSuite:
    def __init__(self, judge: OpenAIQualityJudge, min_faithfulness: float = 0.7, min_pass_rate: float = 80.0):
        self.judge = judge
        self.min_faithfulness = min_faithfulness
        self.min_pass_rate = min_pass_rate

    def run_suite(self, dataset: List[EvalTestCase], app_fn) -> Dict[str, Any]:
        results = []
        for case in dataset:
            actual = app_fn(case.prompt, case.reference_context)
            scores = self.judge.evaluate(case.prompt, case.reference_context, actual)

            faithfulness = scores.get("faithfulness", 0.0)
            relevance = scores.get("relevance", 0.0)
            overall = round((faithfulness + relevance) / 2.0, 2)
            passed = faithfulness >= self.min_faithfulness and overall >= 0.70

            results.append({
                "test_id": case.id,
                "scores": scores,
                "overall": overall,
                "passed": passed,
                "output_snippet": actual[:80] + "...",
            })

        pass_count = sum(1 for r in results if r["passed"])
        pass_rate = (pass_count / max(1, len(dataset))) * 100.0
        ci_passed = pass_rate >= self.min_pass_rate

        return {
            "total": len(dataset),
            "passed_count": pass_count,
            "pass_rate_pct": round(pass_rate, 1),
            "ci_gate_passed": ci_passed,
            "details": results,
        }


# ── Target App Being Evaluated ──
def target_ai_application(prompt: str, context: str) -> str:
    """Target app function being evaluated."""
    if "rag" in prompt.lower():
        return "RAG combines vector database retrieval with LLM generation for grounded answers."
    elif "agent" in prompt.lower():
        return "Agents run an autonomous loop calling external tools to solve complex multi-step tasks."
    return "AI models process tokens to generate text responses."


def main():
    print("=" * 60)
    print("  AI Quality Evaluation Suite (Real OpenAI LLM-as-a-Judge)")
    print("=" * 60 + "\n")

    golden_set = [
        EvalTestCase(
            id="eval-01",
            prompt="Explain RAG",
            reference_context="RAG combines vector database retrieval with LLM generation for grounded answers.",
            expected_answer="Retrieval-Augmented Generation",
        ),
        EvalTestCase(
            id="eval-02",
            prompt="What is an AI agent?",
            reference_context="Agents run an autonomous loop calling external tools to solve complex multi-step tasks.",
            expected_answer="Autonomous loop with tool calling",
        ),
    ]

    judge = OpenAIQualityJudge()
    suite = QualityEvalSuite(judge=judge, min_pass_rate=80.0)
    summary = suite.run_suite(golden_set, target_ai_application)

    print(f"Pass Rate: {summary['pass_rate_pct']}% ({summary['passed_count']}/{summary['total']})")
    print(f"CI Quality Gate: {'✅ PASSED' if summary['ci_gate_passed'] else '❌ FAILED'}\n")

    for d in summary["details"]:
        status = "✅ PASS" if d["passed"] else "❌ FAIL"
        scores = d["scores"]
        print(f"[{status}] {d['test_id']}: Faithfulness={scores.get('faithfulness')} | Relevance={scores.get('relevance')} | Conciseness={scores.get('conciseness')}")
        print(f"        Judge Reasoning: {scores.get('explanation')}")

    if not summary["ci_gate_passed"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
