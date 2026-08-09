"""
Exercise 01: Build an LLM-as-a-Judge Eval Harness (Starter)
============================================================
Course 13 — LLM Evaluation & Quality

Goal: Implement an offline evaluation harness that scores LLM outputs against a golden
      dataset using multi-criteria rubrics (Faithfulness, Relevance, Conciseness) and
      calculates pass/fail quality gates for CI pipelines.

Instructions:
  1. Complete the TODO sections below.
  2. Run: python 01-starter.py
  3. Compare your output with 01-solution.py

Zero external dependencies required — standard library Python only.
"""

import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable


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


class MockLLMJudge:
    """Simulates an LLM Judge scoring an output against reference context and criteria."""

    @staticmethod
    def evaluate(query: str, context: str, response: str) -> Dict[str, float]:
        # Simple heuristic scoring simulator for exercise demonstration
        scores = {}

        # 1. Faithfulness: Is the output grounded in context?
        context_words = set(context.lower().split())
        response_words = set(response.lower().split())
        overlap = len(response_words & context_words) / max(1, len(response_words))
        scores["faithfulness"] = round(min(1.0, overlap * 1.5), 2)

        # 2. Relevance: Does the output address the query keywords?
        query_words = set(query.lower().split()) - {"what", "is", "the", "a", "of", "and", "in", "to"}
        query_match = len(query_words & response_words) / max(1, len(query_words))
        scores["relevance"] = round(min(1.0, query_match * 1.2), 2)

        # 3. Conciseness: Penalty if response exceeds 50 words
        word_count = len(response.split())
        scores["conciseness"] = 1.0 if word_count <= 40 else round(max(0.0, 1.0 - (word_count - 40) * 0.02), 2)

        return scores


class EvalHarness:
    """Automated evaluation test runner for AI Quality Gates."""

    def __init__(self, judge: MockLLMJudge, min_pass_threshold: float = 0.75):
        self.judge = judge
        self.min_pass_threshold = min_pass_threshold

    def score_single(self, test_case: TestCase, generated_answer: str) -> EvalResult:
        """
        TODO: Evaluate a single test case response.
        1. Call self.judge.evaluate(test_case.input_query, test_case.reference_context, generated_answer).
        2. Calculate the overall average score across all metric categories.
        3. Set passed = True if average score >= self.min_pass_threshold AND faithfulness >= 0.6.
        4. Construct and return an EvalResult object.
        """
        pass  # Your code here

    def run_suite(self, test_cases: List[TestCase], app_fn: Callable[[str, str], str]) -> Dict[str, Any]:
        """
        TODO: Run evaluation suite across all test cases.
        1. For each TestCase, generate an output using app_fn(test_case.input_query, test_case.reference_context).
        2. Score the generated output using self.score_single().
        3. Aggregate statistics: total test count, pass count, pass rate %, average score per metric.
        4. Determine overall CI quality gate status: True if pass rate >= 80%.
        """
        pass  # Your code here


# ── Sample App & Run ──────────────────────────────────────────────────
def sample_ai_app(query: str, context: str) -> str:
    """Simulates a RAG application being evaluated."""
    if "rag" in query.lower():
        return "RAG stands for Retrieval-Augmented Generation. It retrieves context from a vector database before generating an answer."
    elif "transformer" in query.lower():
        return "Transformers use multi-head self-attention mechanisms to process tokens in parallel without sequential recurrence."
    else:
        return "I am an AI assistant and I provide general helpful responses to questions."


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

    harness = EvalHarness(judge=MockLLMJudge(), min_pass_threshold=0.75)
    print("--- Running Quality Eval Suite ---")
    summary = harness.run_suite(golden_dataset, sample_ai_app)

    if summary:
        print(f"Pass Rate: {summary['pass_rate']:.1f}%")
        print(f"CI Quality Gate Status: {'✅ PASSED' if summary['ci_gate_passed'] else '❌ FAILED'}")
        print("\n--- Detailed Results ---")
        for res in summary["results"]:
            status = "✅ PASS" if res.passed else "❌ FAIL"
            print(f"[{status}] {res.test_id}: {res.scores} | Reason: {res.reason}")
    else:
        print("TODO: Complete the score_single and run_suite methods!")
