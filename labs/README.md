# Labs — Runnable Code & Hands-on Notebooks

Hands-on Jupyter notebooks that pair directly with the [courses](https://psssnikhil.github.io/ai-engineering-hub/learn/). Reading builds understanding; these build production engineering skills.

---

## Quick Setup

```bash
cd labs
pip install -r requirements.txt

# Set your API keys (OpenAI, Anthropic, or both!)
export OPENAI_API_KEY=sk-proj-...       # https://platform.openai.com
export ANTHROPIC_API_KEY=sk-ant-...    # https://platform.claude.com

jupyter lab
```

---

## Lab Matrix

| Lab | Pairs with | What you build |
|-----|-----------|----------------|
| **[lab-01-rag-from-scratch](lab-01-rag-from-scratch.ipynb)** | Course 06 · RAG | Complete RAG pipeline in ~100 lines: chunking, TF-IDF retrieval, grounded generation with OpenAI (`gpt-4o-mini`) or Claude (`claude-3-5-sonnet`) — no frameworks |
| **[lab-02-agent-loop-from-scratch](lab-02-agent-loop-from-scratch.ipynb)** | Course 07 · AI Agents | ReAct (Reasoning + Acting) tool-calling agent loop supporting OpenAI and Anthropic models with JSON schema parsing and error recovery |
| **[lab-03-eval-harness-from-scratch](lab-03-eval-harness-from-scratch.ipynb)** | Course 13 · LLM Evals | Production-grade LLM-as-a-Judge evaluation harness with G-Eval scoring and CI/CD quality gates |
| **[lab-04-hybrid-search-reranking](lab-04-hybrid-search-reranking.ipynb)** | Course 06 & 10 · Vector DBs | Hybrid sparse BM25 + dense vector search engine with Reciprocal Rank Fusion (RRF) from scratch |

---

## Quality Bar & Contribution Guidelines

We invite community contributions to make these notebooks the highest quality AI engineering reference code available.

### Contribution Requirements:
1. **Zero Framework Bloat**: Implement core mechanics from scratch with pure Python and official SDKs (`openai`, `anthropic`).
2. **Production-Grade Design Patterns**: Include explicit error handling, retries, fallback logic, and clear output schemas.
3. **Comprehensive Markdown Explanations**: Walk the reader through architectural decisions, math, and tradeoffs.
4. **Saved Execution Outputs**: Notebooks submitted via PR must be clean, executable, and include saved cell outputs.

👉 **[View Open Lab Request Issues on GitHub](https://github.com/psssnikhil/ai-engineering-hub/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)** to pick up a lab notebook topic!
