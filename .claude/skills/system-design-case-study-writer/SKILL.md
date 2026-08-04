---
name: system-design-case-study-writer
description: Use when adding or extending AI/ML system design case studies (docs/interview-prep/design-*.md or similar) — e.g. "design a RAG system", "design an LLM serving platform". Produces a full interviewer-style walkthrough (requirements → architecture → tradeoffs → failure modes → scaling), not just an architecture diagram.
---

# System design case study writer

Companion to `curriculum-content-writer` — read that first for repo wiring and
frontmatter rules. This skill is specific to **AI/ML system design case studies** under
`docs/interview-prep/`.

## Why this differs from a normal lesson

A system design interview is scored on *process*, not on landing at one "correct"
architecture. A case study page must model that process, not present a finished diagram
as if it were the only right answer.

## Required structure for every case study

1. **The prompt** — the one-line question as an interviewer would give it (e.g. "Design
   a RAG system for a 50M-document legal corpus with sub-second p99 latency").
2. **Clarifying questions** — 4-6 questions a strong candidate asks before designing
   anything (scale, latency budget, consistency needs, cost ceiling, update frequency).
   State the assumed answers, since the rest of the design depends on them.
3. **Requirements** — functional + non-functional, derived from the clarified answers.
   Include a back-of-envelope numbers table (QPS, data volume, latency budget) — DEPTH_STANDARDS.md
   rewards numerical walkthroughs over abstract prose.
4. **High-level architecture** — a mermaid diagram plus a component-by-component
   walkthrough of what each piece does and why it's there.
5. **Deep dive on 1-2 components** — pick the parts that are actually hard (e.g. chunking
   strategy + retrieval reranking for RAG; KV-cache and batching for LLM serving) and go
   to implementation-level depth there, not everywhere.
6. **Tradeoffs table** — at least one real "Option A vs Option B" with a decision and the
   reasoning, e.g. "hybrid search vs pure vector search — chose hybrid because legal
   queries include exact citation lookups that embeddings miss."
7. **Failure modes & mitigations** — what breaks at scale or under partial outage, and
   how the design handles it (retries, circuit breakers, degraded-mode answers, cache
   staleness).
8. **What a follow-up question probes** — 2-3 likely interviewer follow-ups ("how does
   this change at 10x scale?", "how do you evaluate answer quality in prod?") with short
   answers.
9. **Key takeaways** — 5-8 bullets, per DEPTH_STANDARDS.md.

## Tone

Write as the candidate thinking out loud, not as a finished spec. Show the "why not X"
reasoning at each decision point — that's what DEPTH_STANDARDS.md's "quality patterns"
section calls out explicitly, and it's also literally what's being scored in the real
interview.

## Scope discipline

One case study = one system, end to end. Do not try to cover multiple unrelated systems
in one file — split into separate case-study pages (e.g. `design-rag-system.md`,
`design-agent-platform.md`, `design-llm-serving.md`, `design-eval-pipeline.md`).
