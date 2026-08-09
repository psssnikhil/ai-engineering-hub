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
| 🧭 **Repo Tour & Overview** | *"What is this repo?"* / *"Show me around"* | `repo-onboarding` |
| 🎯 **Personalized Roadmap** | *"Where should I start?"* / *"I want to learn RAG"* | `learning-path-advisor` |
| 💡 **Concept Deep-Dive & Quiz** | *"Explain attention mechanisms"* / *"Quiz me on agents"* | `ai-tutor` |
| ⏱️ **Time-boxed Study Session** | *"I have 2 hours — coach my session"* | `study-session-coach` |
| 🏗️ **Mock System Design Interview** | *"Interview me on RAG system design"* | `mock-interviewer` |
| 🧪 **Lab Code Review & Debug** | *"Review my lab code"* / *"Verify exercise 01"* | `lab-verifier` |

👉 **[Learn how to activate Tutor Skills →](https://psssnikhil.github.io/ai-engineering-hub/learn/using-tutor-skills/)**

---

## ⚡ Quick Links

- 📖 **[Read the Online Handbook](https://psssnikhil.github.io/ai-engineering-hub/)** — 140+ lessons across 16 core courses
- 🚀 **[Start Here Guide](https://psssnikhil.github.io/ai-engineering-hub/start-here/)** — Tailored learning tracks based on your experience
- 🛠️ **[Code Projects (`/labs/projects`)](labs/projects/)** — 12 production reference projects across key domains
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

## 🚀 Realistic Multi-Domain Code Projects (`/labs/projects`)

Framework-free Python reference projects demonstrating production AI systems from zero dependencies to multi-provider enterprise applications:

| # | Project | Domain | Description & Key Capabilities | Link |
|:---|:---|:---|:---|:---|
| **01** | **RAG Pipeline** | General AI | Chunking, vector embeddings, cosine similarity & grounded generation | [`01-rag-pipeline`](labs/projects/01-rag-pipeline/) |
| **02** | **ReAct Agent Loop** | Agent Systems | Tool parsing, multi-provider LLM gateway & observation recovery | [`02-agent-loop`](labs/projects/02-agent-loop/) |
| **03** | **LLM Eval Harness** | Quality & Evals | LLM-as-a-Judge multi-metric scoring (faithfulness & relevance) for CI gates | [`03-eval-harness`](labs/projects/03-eval-harness/) |
| **04** | **Hybrid Search** | Search & Retrieval | BM25 keyword matching + Dense embeddings fused via Reciprocal Rank Fusion | [`04-hybrid-search`](labs/projects/04-hybrid-search/) |
| **05** | **MCP Agent** | Enterprise Tools | Model Context Protocol (MCP) in-memory JSON-RPC server & agent client | [`05-mcp-agent`](labs/projects/05-mcp-agent/) |
| **06** | **Autonomous Agent Platform** | Multi-Agent | Multi-step ReAct agent platform with tool routing & report synthesis | [`06-autonomous-agent-platform`](labs/projects/06-autonomous-agent-platform/) |
| **07** | **Enterprise RAG System** | Production LLMOps | Production RAG assistant with CLI, FastAPI server & automated evals | [`07-enterprise-rag-system`](labs/projects/07-enterprise-rag-system/) |
| **08** | **FinTech Analyst Agent** | Financial Analysis | SEC 10-K filing research, ratio tools (P/E, FCF), & equity report synthesis | [`08-fintech-financial-analyst-agent`](labs/projects/08-fintech-financial-analyst-agent/) |
| **09** | **Healthcare Safety Agent** | Healthcare & Safety | Multi-layer guardrails gateway, emergency triage classifier, & medical RAG | [`09-healthcare-medical-guardrails-agent`](labs/projects/09-healthcare-medical-guardrails-agent/) |
| **10** | **E-Commerce Shopping Copilot**| Retail & Support | Long-term user preference memory, SQL inventory search, & recommendations | [`10-ecommerce-ai-shopping-copilot`](labs/projects/10-ecommerce-ai-shopping-copilot/) |
| **11** | **Code Analysis Assistant** | Developer Tools | Python AST codebase parsing, SQL injection security scanner, & refactoring | [`11-code-analysis-ide-assistant`](labs/projects/11-code-analysis-ide-assistant/) |
| **12** | **Agent Data Flywheel Curator**| AI Infrastructure | Synthetic trajectory curation, rejection sampling filter, & DPO export | [`12-agent-data-flywheel-curator`](labs/projects/12-agent-data-flywheel-curator/) |

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
