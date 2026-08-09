---
title: AI Behavioral & Portfolio Interviews
description: How to talk about AI engineering projects, trade-offs, failures, and evaluations in behavioral rounds
---

# Behavioral & Portfolio Interviews

AI/ML Engineer behavioral rounds focus heavily on your **shipped engineering projects**. Interviewers use this round to differentiate candidates who copy API tutorials from engineers who understand system failure modes, evaluation metrics, cost optimization, and trade-offs.

---

## The 4 Core Probes Interviewers Use

When discussing a project from your portfolio or [Capstone Projects](../advanced/module-17-capstone-projects/index.md), expect deep follow-up questions across these four dimensions:

### 1. Architectural Justification
- *"Why did you use RAG instead of fine-tuning for this task?"*
- *"Why did you choose a vector search database over hybrid BM25 + dense retrieval?"*
- *"What trade-offs led to selecting model X over model Y?"*

### 2. Failure Stories & Incident Response
- *"Tell me about a time your agent got stuck in a loop or executed an invalid tool call."*
- *"How did you handle prompt injection or ungrounded model hallucinations?"*
- *"What was your fallback strategy when the primary model API hit rate limits?"*

### 3. Quantitative Evaluation
- *"How did you measure quality changes before and after changing your chunking strategy?"*
- *"Did you create a golden evaluation dataset? What metrics did you track (Precision@k, MRR, LLM-as-a-judge score)?"*

### 4. Production Economics (Cost & Latency)
- *"What was the per-query token cost and p95 latency?"*
- *"How did you optimize prompt context tokens to fit budget constraints?"*

---

## The STAR+T Storytelling Framework

Structure every project answer in 90 to 120 seconds using **Situation → Task → Action → Result → Trade-offs**:

```markdown
1. Situation: "At [Company/Project], we needed to answer compliance questions over 50k PDFs."
2. Task: "Our goal was <3s latency with 95%+ factual citation accuracy."
3. Action: "I implemented a hybrid BM25 + dense vector retrieval pipeline using Cohere Rerank and a ReAct agent loop."
4. Result: "Reduced hallucination rates by 40% and achieved a p95 latency of 2.1s."
5. Trade-off: "If I built it today, I would add a prompt compaction layer to cut embedding costs by another 30%."
```

---

## Portfolio Checklist

- [ ] **2–3 Deployed Repos**: Public GitHub repos with clean READMEs, architecture diagrams, and runnable setup scripts (see [Build These First](../projects/build-these.md)).
- [ ] **Evaluation Scorecards**: Benchmark metrics included in your project documentation showing model quality comparisons.
- [ ] **Live Demo / Video**: A 1-minute video walk-through demonstrating tool execution or RAG retrieval.