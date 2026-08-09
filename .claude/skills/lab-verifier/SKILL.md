---
name: lab-verifier
description: Verify, grade, and review learner lab code implementations across RAG, AI Agents, Tool Execution, LLMOps, Evals, and Fine-Tuning. Use when the user asks to review their code, test a lab project, verify an exercise solution, or asks "is my RAG/agent code correct?".
---

# Lab Verifier & Code Reviewer Skill

Review learner Python code against AI engineering handbook standards, performance criteria, safety guardrails, and architectural patterns.

## Evaluation Checklist

When evaluating learner code, check against these 5 pillars:

1. **Functional Correctness**: Does the code execute cleanly without unhandled exceptions or infinite loops?
2. **AI Engineering Best Practices**:
   - **RAG**: Proper chunking with overlap, vector normalization, dense + sparse hybrid fallback, and re-ranking.
   - **Agents**: Structured ReAct loop, max-step termination bounds (`max_steps=10`), tool parameter validation, and error recovery.
   - **LLMOps & Serving**: Exponential backoff retry logic, token usage tracking, and streaming handling.
3. **Safety & Security**: Prompt injection sanitization, PII masking, and API key environment variable loading (`os.getenv`).
4. **Code Quality & Typing**: Python 3.10+ type hints (`dataclasses`, `Pydantic`), docstrings, and clean modular structure.
5. **Testability**: Clear assertion boundaries and unit/integration test coverage.

## Verification Steps

1. Read the learner's source code file using `view_file`.
2. Run automated test suites if available: `pytest labs/tests/`.
3. Provide a structured review report with:
   - **Score**: 1–10 Rating across Architecture, Safety, and Correctness.
   - **Strengths**: What was implemented well.
   - **Gaps & Edge Cases**: Unhandled edge cases (e.g. missing API retry, unconstrained loop).
   - **Refactored Snippet**: Crisp code improvements matching production handbook standards.
