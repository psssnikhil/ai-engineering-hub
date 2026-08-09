# CLAUDE.md — AI Engineering Handbook Agent Operating Guide

Welcome! This repository is the **AI Engineering Handbook** — an open-source, interactive curriculum from **Transformers → RAG → Agents → Production Systems → Capstones**.

When connected to Claude Code, Cursor, Antigravity, or any AI assistant, this repository operates as an **interactive AI pair programmer, tutor system, and production blueprint workspace**.

---

## 🤖 Interactive Learner Tutor Skills

Express your goal in chat — the agent automatically loads the matching skill from `.claude/skills/` or `.agents/skills/`:

| What you say in chat | Skill Activated | What Claude Does |
|----------------------|-----------------|------------------|
| *"Where should I start?"* / *"I want to learn RAG"* | `learning-path-advisor` | Routes you through an exact sequence of lessons, labs & projects based on your role. |
| *"Explain attention"* / *"Quiz me on agents"* | `ai-tutor` | Delivers Socratic explanations, tensor shape intuition, worked math, and quiz questions. |
| *"I have 2 hours — coach my session"* | `study-session-coach` | Builds a time-boxed study plan targeting 1 tangible lab/project artifact today. |
| *"Interview me on RAG system design"* | `mock-interviewer` | Conducts a 45-minute whiteboard mock interview with follow-up trade-off questions & scoring. |

**Routing Reference:** `.claude/references/handbook-routing.md`  
**Universal Agent Rules:** `AGENTS.md`  
**Full Guide:** [docs/learn/using-tutor-skills.md](docs/learn/using-tutor-skills.md)

---

## 🛠 Contributor Authoring Skills

When modifying or expanding curriculum content, activate authoring skills:

| Skill | Purpose & Target Directory |
|-------|----------------------------|
| `curriculum-content-writer` | Add or edit handbook courses (`docs/foundations/`, `docs/build/`, `docs/production/`, `docs/advanced/`) following `maintainers/DEPTH_STANDARDS.md`. |
| `interview-question-writer` | Add Q&A banks in `docs/interview-prep/questions-*.md`. |
| `system-design-case-study-writer` | Add end-to-end system design case studies in `docs/interview-prep/design-*.md`. |

---

## 🧪 Executable Code & Multi-Provider Setup (`labs/`)

The repository includes framework-free, pure Python lab notebooks supporting both **OpenAI** and **Anthropic** out of the box:

```bash
cd labs
pip install -r requirements.txt

# Export your preferred API key (or both!)
export OPENAI_API_KEY=sk-proj-...      # https://platform.openai.com
export ANTHROPIC_API_KEY=sk-ant-...   # https://platform.claude.com

jupyter lab
```

### Lab Index:
- `lab-01-rag-from-scratch.ipynb`: Chunking, TF-IDF, grounded LLM generation.
- `lab-02-agent-loop-from-scratch.ipynb`: ReAct tool-calling agent loop & error recovery.
- `lab-03-eval-harness-from-scratch.ipynb`: LLM-as-a-Judge G-Eval rubrics & CI quality gates.
- `lab-04-hybrid-search-reranking.ipynb`: BM25 + Dense vector search + Reciprocal Rank Fusion (RRF).

---

## ⚡ Navigation & Verification Rules

- **Single Source of Truth**: `curriculum.yml`.
- **Sync Command**: `npm run sync-nav` (Updates `mkdocs.yml` nav automatically).
- **Strict Site Build**: `mkdocs build --strict` (Ensures zero broken links or markdown errors).
- **Link Verification**: `node scripts/verify-site-links.mjs`.

> ⚠️ **CRITICAL RULE**: Do **NOT** manually edit the `nav:` block in `mkdocs.yml`. Always edit `curriculum.yml` and run `npm run sync-nav`.

```bash
# Standard Verification Workflow before committing:
npm run sync-nav
mkdocs build --strict
node scripts/verify-site-links.mjs
```

---

## 🧭 Key Entry Points

- `AGENTS.md` — Universal agent workspace rules & skill catalog
- `docs/start-here.md` — Persona-based entry points
- `docs/learn/index.md` — 16 courses in order
- `docs/interview-prep/index.md` — System design case studies & interview question banks
- `docs/resources/index.md` — Curated GitHub repos, videos, blogs, and books
- `maintainers/DEPTH_STANDARDS.md` — Content quality & depth bar
