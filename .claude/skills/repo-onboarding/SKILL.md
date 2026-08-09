---
name: repo-onboarding
description: Onboard a user to the AI Engineering Hub repository. Use when a user is new to the repo, asks "What is this repo?", "How do I navigate this codebase?", "What can I do here?", "Onboard me", "Show me around", "What skills are available?", or needs a complete interactive tour of the repo structure, core courses, labs, system design case studies, and agentic tutor skills.
---

# Repo Onboarding — AI Engineering Hub

Welcome to the **AI Engineering Hub** — an open-source, interactive curriculum and production blueprint covering **Transformers → RAG → Autonomous Agents → Production Systems → Capstones**.

When connected to an AI coding assistant (Claude Code, Cursor, Antigravity, Windsurf, Codex, Aider), this repository functions as an **interactive AI pair programmer, tutor system, and hands-on lab workspace**.

---

## 🌟 What You Can Do With This Repo

1. **Follow Tailored Learning Paths**
   - Study 16 core courses organized into 4 modules (Foundations, Build, Production, Advanced).
   - Explore specialized tracks: **Agent Engineering**, **Modern AI & IDE Agents (2026)**, and **Interview Prep & System Design**.
   - Use persona-based roadmaps for Software Engineers, ML Engineers, or Career Transitioners.

2. **Build & Practice Hands-on Python Labs (`labs/`)**
   - Run pure-Python implementations of key AI mechanisms (ReAct agent loops, attention mechanisms, RAG chunking, vector indexing) without black-box abstractions.
   - Build 12 complete production reference projects in `/labs/projects`.

3. **Master AI System Design & Interview Prep**
   - Review architectural case studies for production systems: RAG platforms, Agent runtimes, Guardrail proxies, LLM serving engines, and Eval pipelines.
   - Practice with curated Q&A banks and whiteboard scenario prompts.

4. **Interact with AI Tutor & Contributor Skills**
   - Activate specialized built-in agent skills for tutoring, session coaching, lab verification, mock interviews, and curriculum contribution.

---

## 🧭 Repository Mental Map

```
.
├── curriculum.yml             # Source of truth for 16 courses, 3 tracks & site nav
├── CLAUDE.md                  # Quick reference & agent operating guide
├── AGENTS.md                  # Workspace rules & universal skill catalog
├── docs/                      # Core handbook content (MkDocs markdown source)
│   ├── foundations/           # Courses 01–05 (GenAI, Essentials, NNs, Transformers, LLMs)
│   ├── build/                 # Courses 06–11 (RAG, Agents, Harness, Multi-agent, Vector DBs, Prompts)
│   ├── production/            # Courses 12–14 (LLMOps, Evals, Safety)
│   ├── advanced/              # Courses 15–16 (Fine-tuning, Capstone Projects)
│   ├── agent-engineering/     # Track: Agent Engineering
│   ├── interview-prep/        # Track: Interview Prep & System Design
│   ├── ai-engineering-2026/   # Track: Modern AI & IDE Agents
│   ├── deep-dives/            # Mathematical & Architectural Deep Dives
│   └── resources/             # Curated AI repos, videos, blogs, and books
├── labs/                      # Pure Python executable notebooks & lab scripts
│   ├── exercises/             # Starter exercises with solution scripts
│   └── projects/              # 12 production reference projects
├── scripts/                   # Nav sync (`sync-nav.mjs`) & link verification tools
├── .claude/skills/            # Claude Code / Cursor Agentic Skills
└── .agents/skills/            # Universal Agentic Skills
```

---

## 🤖 Catalog of Available Agent Skills

This workspace provides specialized agent skills. State your intent to activate them:

### 🎓 Learner & Tutor Skills

| Skill | Trigger Prompts | What It Does |
|-------|-----------------|--------------|
| **`repo-onboarding`** | *"What is this repo?"* / *"Show me around"* / *"Onboard me"* | Complete tour of repo structure, learning paths, labs, and skills (this skill). |
| **`learning-path-advisor`** | *"Where should I start?"* / *"I want to learn RAG"* | Generates a personalized multi-week learning plan with exact lesson links. |
| **`ai-tutor`** | *"Explain self-attention"* / *"Quiz me on agents"* | Provides Socratic explanations, worked math/tensor shape intuition, and quiz questions. |
| **`study-session-coach`** | *"I have 2 hours — coach my session"* | Creates a time-boxed daily study schedule with 1 tangible artifact target. |
| **`mock-interviewer`** | *"Interview me on RAG system design"* | Conducts a 45-minute interactive whiteboard system design interview. |
| **`lab-verifier`** | *"Review my lab code"* / *"Is my RAG code correct?"* | Grades, verifies, and debugs Python lab code implementations against depth standards. |

### 🛠️ Contributor Skills

| Skill | Trigger Prompts | What It Does |
|-------|-----------------|--------------|
| **`curriculum-content-writer`** | *"Add a lesson on MCP tools"* | Authors/edits handbook lessons following `maintainers/DEPTH_STANDARDS.md`. |
| **`interview-question-writer`** | *"Add Q&A on vector databases"* | Authors interview Q&A banks in `docs/interview-prep/`. |
| **`system-design-case-study-writer`** | *"Add case study for agent platform"* | Authors comprehensive system design case studies with trade-offs & scaling. |

---

## 🚀 Suggested Next Steps

Where would you like to begin? Pick one of these options:

1. 🎯 **Get a Personalized Learning Plan**: Say *"Where should I start?"* or *"I want to learn RAG/Agents"*.
2. 💡 **Deep Dive into a Concept**: Say *"Explain attention"* or *"Quiz me on transformers"*.
3. ⏱️ **Schedule Today's Study Session**: Say *"I have 1 hour today — coach my session"*.
4. 💻 **Practice Lab Coding**: Open a starter file in `labs/exercises/` and say *"Verify my lab solution"*.
5. 🏗️ **Practice System Design**: Say *"Interview me on RAG system design"*.
