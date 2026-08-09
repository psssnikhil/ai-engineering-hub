# LLM Fundamentals Q&A

Rapid-fire concepts interviewers actually ask, with pointers to the deep material.

## Core question bank

- Walk me through self-attention. Why scale by √d? → [Transformers & Attention](../foundations/module-06-transformers-attention-mechanisms/index.md), [Attention Math](../deep-dives/attention-math.md)
- What actually happens during fine-tuning vs RAG vs prompting — when do you pick each?
- Explain temperature, top-p, top-k. What breaks at temperature 0?
- Why do LLMs hallucinate? What are the real mitigations (and their limits)?
- What is KV-cache and why does it dominate inference cost?
- Tokenization: why does "strawberry has 3 r's" fail? → [Tokenization Internals](../deep-dives/tokenization-internals.md)
- Context windows: what degrades as they grow? (lost-in-the-middle, cost, latency)
- RLHF vs DPO vs constitutional methods — one-paragraph versions.

## How to answer

State the mechanism in 2–3 sentences, then one engineering consequence. Interviewers are testing whether you can connect theory to shipped systems.

--8<-- "scaffold-note.md"