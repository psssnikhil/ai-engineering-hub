# Labs — Runnable Code

Hands-on Jupyter notebooks that pair with the [courses](https://psssnikhil.github.io/ai-engineering-handbook/learn/). Reading builds understanding; these build skill.

## Setup

```bash
cd labs
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...   # https://platform.claude.com
jupyter lab
```

## Labs

| Lab | Pairs with | What you build |
|-----|-----------|----------------|
| [lab-01-rag-from-scratch](lab-01-rag-from-scratch.ipynb) | Course 06 · RAG | A complete RAG pipeline in ~100 lines: chunking, TF-IDF retrieval, grounded generation with Claude — no frameworks |
| lab-02-agent-loop *(planned)* | Course 07 · AI Agents | A tool-using agent loop from scratch |
| lab-03-eval-harness *(planned)* | Course 13 · Evals | A golden-set eval suite with LLM-as-judge |

## Principles

- **No frameworks first.** Every lab builds the core mechanism by hand before mentioning LangChain/LlamaIndex — you should understand what the framework abstracts.
- **Cheap to run.** Labs minimize API calls; a full run of lab-01 costs a few cents.
- **Interview-ready.** Each lab maps to a common [coding-round question](https://psssnikhil.github.io/ai-engineering-handbook/interview-prep/coding-rounds/).

Want to contribute a lab? See [CONTRIBUTING](../.github/CONTRIBUTING.md) — planned labs above are up for grabs.
