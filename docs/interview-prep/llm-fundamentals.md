---
title: LLM Fundamentals Q&A Overview
description: Core LLM concepts, attention mechanisms, sampling parameters, and fine-tuning vs RAG for interview prep
---

# LLM Fundamentals Q&A Overview

A collection of rapid-fire technical questions frequently asked during screening and technical deep-dive rounds for AI/ML roles.

---

## 8 Essential Concepts Every AI Engineer Must Defend

| Question | Core Mechanism | Engineering Consequence | Deep Dive |
|----------|----------------|------------------------|-----------|
| **Why scale dot-product attention by \(\sqrt{d_k}\)?** | Prevents dot products from growing large in high dimensions, keeping softmax gradients out of near-zero saturation regions. | Maintains stable gradient flow during Transformer training. | [Attention Math](../deep-dives/attention-math.md) |
| **When to pick RAG vs Fine-tuning?** | RAG injects dynamic external context; fine-tuning updates internal parametric weights for style/task adaptation. | RAG is cheaper for volatile data; fine-tuning excels at specialized formatting/behavior. | [RAG vs Fine-tuning](../faq.md) |
| **Explain Temperature, Top-P, and Top-K sampling.** | Temperature scales logits before softmax; Top-K truncates to top \(K\) candidates; Top-P samples from cumulative probability mass. | Low temperature increases determinism; high temperature boosts creativity at the cost of coherence. | [Sampling Lessons](../foundations/module-07-large-language-models-llms/index.md) |
| **What is the KV-Cache bottleneck?** | Stores Key and Value tensors for previous tokens to avoid redundant attention recomputation. | Dictates GPU memory consumption during inference; requires PagedAttention to optimize. | [LLM Serving System Design](design-llm-serving.md) |
| **Why do LLMs struggle with "How many r's in strawberry"?** | Byte-Pair Encoding (BPE) tokenizers group characters into token chunks (e.g. `straw` + `berry`), obscuring individual characters. | Demonstrates sub-word tokenization boundaries and reasoning limits. | [Tokenization Internals](../deep-dives/tokenization-internals.md) |
| **What is the "Lost in the Middle" phenomenon?** | Attention scores favor tokens at the extreme beginning and end of long prompts, degrading retrieval accuracy in the middle. | Requires query re-ordering or reranking to keep relevant context near the prompt boundaries. | [RAG Q&A Bank](questions-rag.md) |
| **Compare SFT, RLHF, and DPO.** | SFT trains on supervised examples; RLHF uses a reward model + PPO; DPO directly optimizes preference loss without a reward model. | DPO simplifies alignment training stability and reduces compute overhead. | [LLM Fundamentals Q&A Bank](questions-llm-fundamentals.md) |
| **What causes hallucinations and how to mitigate?** | Probabilistic next-token generation over sparse training data; mitigated via grounded RAG, constrained JSON output, and self-critique. | Pure prompting cannot completely eliminate hallucinations without external verification. | [Evals & Production Q&A](questions-evals-production.md) |

---

## Comprehensive Question Bank

For full worked answers with follow-ups and candidate scoring rubrics, visit the **[LLM & Transformer Fundamentals Question Bank](questions-llm-fundamentals.md)**.