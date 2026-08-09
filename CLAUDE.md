# CLAUDE.md — AI Engineering Hub Agent Operating Guide

Welcome! This repository is the **AI Engineering Hub** — an open-source, interactive curriculum covering **Transformers → RAG → Agents → Production Systems → Capstones**.

When connected to Claude Code, Cursor, Antigravity, Windsurf, Codex, or any AI assistant, this repository operates as an **interactive AI pair programmer, tutor system, and production blueprint workspace**.

---

## 🤖 Core Agent Philosophy & Operating Principles

1. **Verification-First Execution**: Never declare a task complete without executing empirical build, nav-sync, and link verification commands.
2. **Socratic & Deep Pedagogical Standard**: Every concept must bridge intuitive mental models, mathematical rigor, worked tensor/numerical examples, runnable code, and real-world production trade-offs.
3. **Zero-Fluff Quality Bar**: Avoid marketing buzzwords, ungrounded code, or superficial placeholders. All content must adhere to `maintainers/DEPTH_STANDARDS.md`.
4. **Single Source of Truth**: Site navigation is governed strictly by `curriculum.yml`. Never edit `nav:` in `mkdocs.yml` directly.

---

## 🧭 Repository Mental Map

```
.
├── curriculum.yml             # Source of truth for 16 courses, 3 tracks & site nav
├── CLAUDE.md                  # Quick reference & agent operating guide (this file)
├── AGENTS.md                  # Universal workspace rules & skill catalog
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
├── scripts/                   # Nav sync (`sync-nav.mjs`) & link verification tools
├── .claude/skills/            # Claude Code / Cursor agentic skills
├── .agents/skills/            # Universal agentic skills
└── maintainers/               # Depth standards & repository guidelines
```

---

## ⚡ Autonomous Learner & Contributor Skill Matrix

When a user prompt matches a trigger, load and follow the corresponding skill instructions from `.claude/skills/<skill-name>/SKILL.md` or `.agents/skills/<skill-name>/SKILL.md`:

| Trigger / User Intent | Activated Skill | Target Path & Action |
|-----------------------|-----------------|----------------------|
| *"Where should I start?"* / *"I want to learn RAG"* | `learning-path-advisor` | Route learner through exact sequence of lessons & projects based on role. |
| *"Explain attention"* / *"Quiz me on agents"* | `ai-tutor` | Deliver Socratic explanation, tensor shape intuition, worked math, and quiz questions. |
| *"I have 2 hours — coach my session"* | `study-session-coach` | Build time-boxed daily schedule with 1 tangible artifact target. |
| *"Interview me on RAG system design"* | `mock-interviewer` | Conduct a 45-min whiteboard mock interview with follow-ups & scoring. |
| Add/edit handbook lesson or track | `curriculum-content-writer` | Write/update docs following `DEPTH_STANDARDS.md` and sync nav. |
| Add interview Q&A bank | `interview-question-writer` | Add Q&A in `docs/interview-prep/questions-*.md`. |
| Add system design case study | `system-design-case-study-writer` | Add case study in `docs/interview-prep/design-*.md`. |

**Routing Reference:** `.claude/references/handbook-routing.md`  
**Full Guide:** [docs/learn/using-tutor-skills.md](docs/learn/using-tutor-skills.md)

---

## 🛠 Engineering & Content Quality Standards

### 1. Python Code Standards (`labs/`)
- **Framework-Light & Pure Python**: Prioritize plain Python & standard library implementations for core mechanisms (e.g. attention, RAG, ReAct loop) so learners understand fundamental mechanisms without black-box magic.
- **Multi-Provider API Support**: Support both OpenAI, Anthropic, and Gemini out of the box. Use safe fallback checks:
  ```python
  import os
  openai_key = os.getenv("OPENAI_API_KEY")
  anthropic_key = os.getenv("ANTHROPIC_API_KEY")
  gemini_key = os.getenv("GEMINI_API_KEY")
  ```
- **Type Annotations & Tensor Shapes**: Annotate function parameters, return types, and explicit tensor dimensions in comments (e.g., `# (batch_size, seq_len, d_model)`).

### 2. Markdown & LaTeX Standards (`docs/`)
- **LaTeX Math Delimiters**: Always use MathJax/Arthmatex delimiters:
  - Inline Math: `\( \text{Attention}(Q,K,V) \)`
  - Block Math: `\[ \text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V \]`
  - **CRITICAL**: Do **NOT** use single `$...$` for inline math — dollar amounts (e.g. `$0.04`) break rendering.
- **Admonitions & Alerts**: Use GitHub alerts for callouts:
  - `> [!NOTE]` — Background context or key details
  - `> [!TIP]` — Best practices & efficiency suggestions
  - `> [!IMPORTANT]` — Essential requirements & critical takeaways
  - `> [!WARNING]` — Edge cases & common pitfalls
- **Mermaid Diagrams**: Ensure node labels with special characters or parentheses are enclosed in double quotes (e.g., `id["Query Matrix (Q)"]`).

---

## 🧪 Pre-Commit Verification Workflow

Before declaring any change complete or committing code, run the full verification pipeline:

```bash
# 1. Sync Site Navigation (Generates mkdocs.yml nav from curriculum.yml)
npm run sync-nav

# 2. Strict MkDocs Site Build (Catches markdown formatting & broken links)
mkdocs build --strict

# 3. Verify Internal & Relative Links
node scripts/verify-site-links.mjs

# 4. Verify Python Labs (If labs/ files were edited)
pytest labs/
```

> ⚠️ **CRITICAL RULE**: Never manually edit the `nav:` section in `mkdocs.yml`. Always modify `curriculum.yml` and run `npm run sync-nav`.

---

## 🔍 Agent Diagnostic & Troubleshooting SOP

If a verification command fails, follow these automated diagnostic steps:

1. **`mkdocs build --strict` failure**:
   - Check if a newly added markdown file is listed in `curriculum.yml`.
   - Check for relative link syntax errors or broken image paths.
   - Verify LaTeX delimiters (`\( ... \)` and `\[ ... \]`).
2. **`verify-site-links.mjs` failure**:
   - Trace the exact line reported in the log output.
   - Ensure header anchors (e.g., `#prerequisites`) match the exact generated anchor string.
3. **`npm run sync-nav` failure**:
   - Validate YAML syntax in `curriculum.yml` using a strict parser or check for missing titles/paths.
