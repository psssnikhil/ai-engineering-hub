# Handbook routing reference

Compact index for learner tutor skills. **Always prefer live files** when the user
names a specific topic — this is a routing cheat sheet, not the source of truth.

Primary navigation files to read when routing:

| File | Use for |
|------|---------|
| `docs/start-here.md` | Persona + goal → first courses |
| `docs/learn/study-plans.md` | Week-by-week schedules (beginner / intermediate / agent engineer) |
| `docs/topic-map.md` | Concept → course lookup |
| `docs/learn/index.md` | Full 16-course ordered list |
| `curriculum.yml` | Canonical course titles + folder paths |
| `docs/projects/build-these.md` | Portfolio projects mapped to courses |
| `docs/interview-prep/` | Interview Q&A + system design case studies |
| `docs/deep-dives/` | Math-heavy supplements (attention, backprop, tokenization) |
| `docs/glossary.md` | Term definitions |
| `docs/faq.md` | RAG vs fine-tune vs agents decisions |

## 16 core courses (ordered)

| # | Title | Path |
|---|-------|------|
| 01 | GenAI Foundations | `docs/foundations/module-00-genai-foundations-from-nlp-to-transformers/` |
| 02 | AI Engineering Essentials | `docs/foundations/module-01-ai-engineering-essentials/` |
| 03 | Neural Networks & Deep Learning | `docs/foundations/module-05-neural-networks-deep-learning-fundamentals/` |
| 04 | Transformers & Attention | `docs/foundations/module-06-transformers-attention-mechanisms/` |
| 05 | Large Language Models | `docs/foundations/module-07-large-language-models-llms/` |
| 06 | RAG | `docs/build/module-09-rag-retrieval-augmented-generation/` |
| 07 | AI Agents | `docs/build/module-11-ai-agents-fundamentals/` |
| 08 | Agent Harness & Runtime | `docs/build/module-18-agent-harness-tools-runtime/` |
| 09 | Multi-Agent Systems | `docs/build/module-12-multi-agent-systems/` |
| 10 | Vector Databases | `docs/build/module-13-vector-databases-deep-dive/` |
| 11 | Prompt Engineering | `docs/build/module-14-prompt-engineering-mastery/` |
| 12 | LLMOps & Production | `docs/production/module-10-llmops-production-systems/` |
| 13 | LLM Evaluation & Quality | `docs/production/module-19-llm-evaluation-quality/` |
| 14 | AI Safety & Ethics | `docs/production/module-16-ai-safety-ethics/` |
| 15 | Fine-Tuning & Custom Models | `docs/advanced/module-15-fine-tuning-custom-models/` |
| 16 | Capstone Projects | `docs/advanced/module-17-capstone-projects/` |

## Optional tracks

| Track | Path | Best for |
|-------|------|----------|
| Agent Engineering | `docs/agent-engineering/` | Production agents: loop, memory, tools, harness, orchestration, evals |
| Interview Prep & System Design | `docs/interview-prep/` | Job interviews, whiteboard system design |
| Modern AI (2026) | `docs/ai-engineering-2026/` | Claude Code, skills, context/loop engineering |

## Goal → starting point

| User goal | Start here | Then | Build |
|-----------|------------|------|-------|
| Understand how LLMs work | 01 → 04 → 05 | `docs/deep-dives/` | Course 04 exercises |
| Call LLM APIs in production | 02 | 12 | Project 1 (Doc Q&A) |
| Build RAG over my documents | 06 | 10, 12 | Project 2 (Enterprise RAG) |
| Build AI agents | Agent Engineering track or 07 | 08 | Project 4 (Tool-using agent) |
| Ship multi-agent systems | 09 | 13 | Project 5 |
| Fine-tune a model | 15 | 05 fine-tuning lessons | Project 8 |
| Evaluate & monitor LLM apps | 13 | `docs/evals-observability/` | Project 9 |
| Use Claude Code / IDE agents | `docs/ai-engineering-2026/` | skills-and-rules.md | Custom repo skill |
| Get a job in AI engineering | `docs/start-here.md` → Learn | `docs/projects/build-these.md` | 3 projects + 16 |
| Prep for interviews | `docs/interview-prep/` | Weak-topic courses from Q&A | Mock system design on whiteboard |

## Persona → study plan

| Persona | Background | Plan file section | Duration |
|---------|------------|-------------------|----------|
| Beginner | SWE, little ML | `docs/learn/study-plans.md` → Beginner (~20 weeks) | 8–10 hrs/week |
| Intermediate | Knows ML/Python, new to LLMs | Intermediate (~12 weeks) | 6–8 hrs/week |
| Agent engineer | Shipping agent systems | Agent engineer (~8 weeks) | 5–7 hrs/week |

## Concept → primary page

| Concept | Primary | Deep dive / hub |
|---------|---------|-----------------|
| Attention / transformers | 04 | `docs/deep-dives/attention-math.md` |
| Tokenization | 05 | `docs/deep-dives/tokenization-internals.md` |
| Backprop / NN math | 03 | `docs/deep-dives/backpropagation-calculus.md` |
| RAG / retrieval | 06 | 10, interview-prep/questions-rag.md |
| Vector search | 10 | 06 hybrid-search lesson |
| Agents / ReAct | 07 | agent-engineering/01-agent-loop.md |
| Tools & MCP | 08 | agent-engineering/03-tools-and-mcp.md |
| Harness / termination | 08 | agent-engineering/04-harness-engineering.md |
| Multi-agent | 09 | agent-engineering/05-orchestration.md |
| Evals | 13 | agent-engineering/07-agent-evals.md |
| Safety / injection | 14 | production safety lessons |
| LLMOps / serving | 12 | interview-prep/design-llm-serving.md |
| Prompting | 11 | 02 lesson 04 |
| Context engineering | ai-engineering-2026/context-engineering.md | agent-engineering/02-memory.md |

## Prerequisite chains (do not skip)

```
Complete beginner:  Prerequisites → 01 → 02 → 06 → 07
Software engineer:  02 → 06 → 07 → 08
ML engineer:        05 → 06 (and/or 15)
Agents in prod:     07 → 08 → 09 → 13
RAG in prod:        06 → 10 → 12 → 13
```

## Stuck? → redirect

| Symptom | Send to |
|---------|---------|
| Math too hard | `docs/deep-dives/` |
| Agent loops forever | agent-engineering/04-harness-engineering.md |
| Bad RAG answers | 06 lesson 08-RAG-Evaluation-Metrics.md |
| Don't know RAG vs fine-tune | docs/faq.md |
| Term unclear | docs/glossary.md |
| Need a project idea | docs/projects/build-these.md |

## Portfolio rule of three

For job seekers: ship **one RAG app**, **one agent**, **one production demo with evals**
— stronger than finishing every lesson without building. See `docs/projects/build-these.md`.

## Site URLs (deployed)

Base: `https://psssnikhil.github.io/learn-ai-engineering/` (may redirect to
`ai-engineering-handbook` — use repo-relative paths in Cursor/Claude Code sessions).
