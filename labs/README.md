# Labs — Runnable Code & Hands-on Notebooks

Hands-on Jupyter notebooks that pair directly with the [courses](https://psssnikhil.github.io/ai-engineering-handbook/learn/). Reading builds understanding; these build production engineering skills.

---

## Quick Setup

```bash
cd labs
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...   # https://platform.claude.com
jupyter lab
```

---

## Lab Matrix

| Lab | Pairs with | What you build |
|-----|-----------|----------------|
| **[lab-01-rag-from-scratch](lab-01-rag-from-scratch.ipynb)** | Course 06 · RAG | Complete RAG pipeline in ~100 lines: chunking, TF-IDF retrieval, grounded generation with Claude — no frameworks |
| **[lab-02-agent-loop-from-scratch](lab-02-agent-loop-from-scratch.ipynb)** | Course 07 · AI Agents | ReAct (Reasoning + Acting) tool-calling agent loop with JSON schema parsing and error recovery |
| **[lab-03-eval-harness-from-scratch](lab-03-eval-harness-from-scratch.ipynb)** | Course 13 · LLM Evals | Production-grade LLM-as-a-Judge evaluation harness with G-Eval scoring and CI/CD quality gates |

---

## Principles

1. **No Frameworks First**: Every lab implements core mechanisms from scratch using Python primitives before introducing high-level frameworks (LangChain, LlamaIndex, Ragas).
2. **Cheap & Lightweight**: Designed to run efficiently in minutes for pennies of API cost.
3. **Interview & Production Ready**: Each lab maps directly to real-world [coding interview questions](https://psssnikhil.github.io/ai-engineering-handbook/interview-prep/coding-rounds/) and production system requirements.
