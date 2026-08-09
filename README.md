<div align="center">

# AI Engineering Hub

### Master Production AI Systems & Autonomous Agent Architecture.

**The open-source curriculum and handbook covering Transformers → RAG → Agentic Systems → Production LLMOps → System Design.**

[![Read Handbook](https://img.shields.io/badge/📖_Read_Handbook-indigo?style=for-the-badge)](https://psssnikhil.github.io/ai-engineering-hub/)
[![Start Here](https://img.shields.io/badge/→_Start_Here-6366f1?style=for-the-badge&labelColor=4338ca)](https://psssnikhil.github.io/ai-engineering-hub/start-here/)
[![GitHub stars](https://img.shields.io/github/stars/psssnikhil/ai-engineering-hub?style=flat-square&logo=github&label=Stars)](https://github.com/psssnikhil/ai-engineering-hub)
[![MIT License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)

</div>

---

## 🤖 Built-in AI Tutor Skills

Turn your AI coding assistant (**Claude Code, Cursor, Antigravity, Windsurf**) into an interactive Socratic tutor while learning from this repository:

| Objective | What to ask / trigger prompt | Activated Tutor Skill |
|:---|:---|:---|
| 🎯 **Personalized Roadmap** | *"Where should I start?"* / *"I want to learn RAG"* | `learning-path-advisor` |
| 💡 **Concept Deep-Dive & Quiz** | *"Explain attention mechanisms"* / *"Quiz me on agents"* | `ai-tutor` |
| ⏱️ **Time-boxed Study Session** | *"I have 2 hours — coach my session"* | `study-session-coach` |
| 🏗️ **Mock System Design Interview** | *"Interview me on RAG system design"* | `mock-interviewer` |

👉 **[Learn how to activate Tutor Skills →](https://psssnikhil.github.io/ai-engineering-hub/learn/using-tutor-skills/)**

---

## ⚡ Quick Links

- 📖 **[Read the Online Handbook](https://psssnikhil.github.io/ai-engineering-hub/)** — 140+ lessons across 16 core courses
- 🚀 **[Start Here Guide](https://psssnikhil.github.io/ai-engineering-hub/start-here/)** — Tailored learning tracks based on your experience
- 🛠️ **[Code Labs (`/labs`)](labs/labs/)** — Framework-free, pure Python reference implementations
- 🎯 **[Interview & System Design](https://psssnikhil.github.io/ai-engineering-hub/interview-prep/)** — Production architecture case studies & Q&A banks

---

## 🗺️ Curriculum Overview

```
  1. FOUNDATIONS            2. BUILD                 3. PRODUCTION         4. ADVANCED
  ──────────────            ───────                  ─────────────         ───────────
  01 GenAI             →    06 RAG              →    12 LLMOps        →    15 Fine-Tuning
  02 AI Essentials     →    07 Agents           →    13 Evals         →    16 Capstone Projects
  03 Neural Nets       →    08 Agent Harness    →    14 Safety
  04 Transformers      →    09 Multi-Agent
  05 LLMs              →    10 Vector DBs
                            11 Prompts
```

### Focused Tracks & Deep Dives
* 🤖 **[Agent Engineering Track](https://psssnikhil.github.io/ai-engineering-hub/agent-engineering/)**: ReAct loops, Memory systems, MCP tools, Harness runtime, & Observability.
* ⚡ **[Modern AI & IDE Agents (2026)](https://psssnikhil.github.io/ai-engineering-hub/ai-engineering-2026/)**: Claude Code, Context engineering, Loop design, & Agentic skills.
* 📐 **[Interview Prep & System Design](https://psssnikhil.github.io/ai-engineering-hub/interview-prep/)**: Whiteboard case studies (RAG, Agent Platform, Guardrails, LLM Serving).

---

## 💻 Code Labs (`/labs/labs`)

Pure Python, zero-framework reference implementations designed to reveal the inner mechanics of AI systems:

| Lab | Topic & Scope | Link |
|:---|:---|:---|
| **Lab 01** | **RAG Pipeline**: Chunking, OpenAI vector embeddings, cosine similarity & grounded generation | [`01_rag_from_scratch.py`](labs/labs/01_rag_from_scratch.py) |
| **Lab 02** | **ReAct Agent Loop**: Tool parsing, multi-provider LLM gateway, observation loop & fallback recovery | [`02_agent_loop_from_scratch.py`](labs/labs/02_agent_loop_from_scratch.py) |
| **Lab 03** | **LLM Eval Harness**: LLM-as-a-Judge multi-metric scoring (faithfulness & relevance) for CI/CD gates | [`03_eval_harness_from_scratch.py`](labs/labs/03_eval_harness_from_scratch.py) |
| **Lab 04** | **Hybrid Search & RRF**: BM25 keyword matching + Dense embeddings fused via Reciprocal Rank Fusion | [`04_hybrid_search_reranking.py`](labs/labs/04_hybrid_search_reranking.py) |
| **Lab 05** | **Model Context Protocol (MCP)**: In-memory MCP Server, JSON-RPC 2.0 protocol dispatch & agent client | [`05_mcp_agent_integration.py`](labs/labs/05_mcp_agent_integration.py) |

---

## 🚀 Run Locally

```bash
git clone https://github.com/psssnikhil/ai-engineering-hub.git
cd ai-engineering-hub
pip install -r requirements.txt
npm install
npm run sync-nav
mkdocs serve
```
Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser.

---

## 🤝 Contributing

We welcome community contributions! Whether improving lesson clarity, fixing code examples, adding case studies, or expanding tutor skills:

- 📖 **[Contribution Guide](docs/contribute.md)** — Curriculum structure, depth standards, and guidelines.
- 🛠️ **[Full Guidelines](.github/CONTRIBUTING.md)** — Code fence standards and PR verification workflow.
- 💡 **[Open Issues](https://github.com/psssnikhil/ai-engineering-hub/issues)** — Find good first issues or suggest new topics.

---

## 🤝 1:1 Mentorship & Enterprise AI Consulting

Looking for personalized 1:1 mentorship or enterprise AI advisory from **Nikhil Pentapalli**?

- 🎯 **1:1 Guidance & Mock Interviews**: Book a 1:1 session on [Topmate](https://topmate.io/nikhil_pentapalli) for career coaching and AI system design practice.
- 🏢 **Enterprise AI Consulting**: For system design reviews, agent platform architecture, RAG systems, and team workshops, email **[psss.nikhil@gmail.com](mailto:psss.nikhil@gmail.com)**.

---

<div align="center">

**[★ Star on GitHub](https://github.com/psssnikhil/ai-engineering-hub)** to support open-source AI education!

Distributed under the **MIT License**.

</div>
