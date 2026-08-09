"""
Exercise 01: Build an LLM-as-a-Judge Eval Harness (Solution)
============================================================
Course 13 — LLM Evaluation & Quality

Uses real OpenAI API (gpt-4o-mini) to score outputs against golden datasets.
"""

import json
from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Callable
from openai import OpenAI


@dataclass
class TestCase:
    id: str
    input_query: str
    reference_context: str
    expected_answer: str


@dataclass
class EvalResult:
    test_id: str
    generated_answer: str
    scores: Dict[str, float]
    passed: bool
    reason: str


class RealLLMJudge:
    """Production LLM-as-a-Judge evaluating against multi-criteria rubrics using OpenAI."""

    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model

    def evaluate(self, query: str, context: str, response: str) -> Dict[str, Any]:
        system_prompt = (
            "You are an expert AI Quality Judge. Evaluate the response against the user query and context. "
            "Return JSON with scores (0.0 to 1.0) for: 'faithfulness' (groundedness), 'relevance', and 'conciseness'."
        )

        user_content = f"Query: {query}\nContext: {context}\nResponse: {response}"

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            response_format={"type": "json_object"},
            temperature=0.0,
        )

        try:
            return json.loads(completion.choices[0].message.content)
        except json.JSONDecodeError:
            return {"faithfulness": 0.0, "relevance": 0.0, "conciseness": 0.0}


class EvalHarness:
    """Automated evaluation test runner for AI Quality Gates."""

    def __init__(self, judge: RealLLMJudge, min_pass_threshold: float = 0.70):
        self.judge = judge
        self.min_pass_threshold = min_pass_threshold

    def score_single(self, test_case: TestCase, generated_answer: str) -> EvalResult:
        scores = self.judge.evaluate(
            test_case.input_query, test_case.reference_context, generated_answer
        )
        faithfulness = float(scores.get("faithfulness", 0.0))
        relevance = float(scores.get("relevance", 0.0))
        conciseness = float(scores.get("conciseness", 0.0))

        avg_score = (faithfulness + relevance + conciseness) / 3.0
        passed = (avg_score >= self.min_pass_threshold) and (faithfulness >= 0.6)

        reason = (
            f"Avg score {avg_score:.2f} >= {self.min_pass_threshold}"
            if passed
            else f"Avg score {avg_score:.2f} below threshold or ungrounded"
        )

        return EvalResult(
            test_id=test_case.id,
            generated_answer=generated_answer,
            scores={"faithfulness": faithfulness, "relevance": relevance, "conciseness": conciseness},
            passed=passed,
            reason=reason,
        )

    def run_suite(self, test_cases: List[TestCase], app_fn: Callable[[str, str], str]) -> Dict[str, Any]:
        results: List[EvalResult] = []

        for case in test_cases:
            answer = app_fn(case.input_query, case.reference_context)
            res = self.score_single(case, answer)
            results.append(res)

        pass_count = sum(1 for r in results if r.passed)
        pass_rate = (pass_count / max(1, len(test_cases))) * 100.0
        ci_gate_passed = pass_rate >= 66.0

        return {
            "total_tests": len(test_cases),
            "pass_count": pass_count,
            "pass_rate": pass_rate,
            "ci_gate_passed": ci_gate_passed,
            "results": results,
        }


def sample_ai_app(query: str, context: str) -> str:
    """Target RAG application being evaluated."""
    query_lower = query.lower()
    if "rag" in query_lower:
        return "RAG stands for Retrieval-Augmented Generation combining vector search with LLMs."
    elif "transformer" in query_lower:
        return "Transformers process all tokens simultaneously using self-attention rather than recurrent steps."
    else:
        return "Mars has no capital city or human settlements."


if __name__ == "__main__":
    golden_dataset = [
        TestCase(
            id="test-01",
            input_query="What does RAG stand for?",
            reference_context="RAG is Retrieval-Augmented Generation combining vector search with LLMs.",
            expected_answer="Retrieval-Augmented Generation",
        ),
        TestCase(
            id="test-02",
            input_query="How do Transformers handle tokens?",
            reference_context="Transformers process all tokens simultaneously using self-attention rather than recurrent steps.",
            expected_answer="Self-attention mechanisms",
        ),
        TestCase(
            id="test-03",
            input_query="What is the capital of Mars?",
            reference_context="Mars has no capital city or human settlements.",
            expected_answer="Mars does not have a capital.",
        ),
    ]

    judge = RealLLMJudge()
    harness = EvalHarness(judge=judge, min_pass_threshold=0.70)
    print("--- Running Real OpenAI LLM-as-a-Judge Eval Suite ---")
    summary = harness.run_suite(golden_dataset, sample_ai_app)

    print(f"Pass Rate: {summary['pass_rate']:.1f}% ({summary['pass_count']}/{summary['total_tests']})")
    print(f"CI Quality Gate Status: {'✅ PASSED' if summary['ci_gate_passed'] else '❌ FAILED'}\n")
    for res in summary["results"]:
        status = "✅ PASS" if res.passed else "❌ FAIL"
        print(f"[{status}] {res.test_id}: {res.scores} | Reason: {res.reason}")
