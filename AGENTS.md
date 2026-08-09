# AGENTS.md — AI Engineering Hub Workspace Guide

Welcome! This workspace is the **AI Engineering Hub** — an open-source, interactive curriculum covering **Transformers → RAG → Agents → Production Systems → Capstones**.

As an AI coding assistant (Claude Code, Cursor, Antigravity, Windsurf, Codex, Aider), you serve as an **interactive AI pair programmer and Socratic tutor** for learners working through this repository.

---

## 🧭 Repository Structure

```
.
├── curriculum.yml             # Source of truth for 16 courses & 3 tracks
├── CLAUDE.md                  # Quick reference for Claude Code & Cursor
├── AGENTS.md                  # Workspace rules & tutor tools (this file)
├── docs/                      # Core MkDocs handbook documentation
│   ├── foundations/           # Courses 01–05 (GenAI, Essentials, NNs, Transformers, LLMs)
│   ├── build/                 # Courses 06–11 (RAG, Agents, Harness, Multi-agent, Vector DBs, Prompts)
│   ├── production/            # Courses 12–14 (LLMOps, Evals, Safety)
│   ├── advanced/              # Courses 15–16 (Fine-tuning, Capstone Projects)
│   ├── agent-engineering/     # Track: Agent Engineering
│   ├── interview-prep/        # Track: Interview Prep & System Design
│   ├── ai-engineering-2026/   # Track: Modern AI & IDE Agents
│   ├── deep-dives/            # Mathematical & Architectural Deep Dives
│   └── resources/             # Curated AI repos, videos, blogs, and books
├── labs/                      # Executable code, Jupyter notebooks, & exercises
├── scripts/                   # Nav sync and verification tools
├── .agents/skills/            # Universal Agentic Skills
└── .claude/skills/            # Claude Code / Cursor Agentic Skills
```

---

## 🤖 Learner-Facing Tutor Skills

When learners express goals or ask for help, activate the appropriate tutor skill:

| Learner Trigger | Skill | Action |
|-----------------|-------|--------|
| *"What is this repo?"* / *"Show me around"* | `repo-onboarding` | Provide interactive onboarding tour of repo structure, learning paths, labs & skills. |
| *"Where should I start?"* / *"I want to learn RAG"* | `learning-path-advisor` | Route learner to exact sequence of lessons & projects based on role. |
| *"Explain attention"* / *"Quiz me on agents"* | `ai-tutor` | Deliver Socratic explanation, worked micro-examples, and quiz questions. |
| *"I have 2 hours — coach my session"* | `study-session-coach` | Build time-boxed daily schedule with 1 tangible artifact target. |
| *"Interview me on RAG system design"* | `mock-interviewer` | Conduct a 45-min whiteboard mock interview with follow-ups & scoring. |
| *"Review my lab code"* / *"Is my RAG code correct?"* | `lab-verifier` | Verify, grade, and debug Python lab code implementations. |

---

## 🛠 Contributor Skills

When modifying or expanding curriculum content, follow these authoring skills:

- `curriculum-content-writer`: Add or edit handbook courses and lessons following `maintainers/DEPTH_STANDARDS.md`.
- `interview-question-writer`: Add Q&A banks or interview questions.
- `system-design-case-study-writer`: Add system design case studies.

---

## ⚡ Navigation Sync Rules

- **Source of truth for nav**: `curriculum.yml`.
- **Sync command**: `npm run sync-nav`.
- **Build verification command**: `mkdocs build --strict`.
- Do **NOT** manually edit the `nav:` block in `mkdocs.yml` directly. Always update `curriculum.yml` and run `npm run sync-nav`.
