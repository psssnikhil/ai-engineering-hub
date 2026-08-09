# AI Engineering Handbook — Claude Code

Open-source curriculum: transformers → RAG → agents → production.

## For learners (use these skills)

This repo ships **tutor skills** in `.claude/skills/`. Express your goal in chat — Claude
loads the matching skill and routes you through existing material.

| Say something like… | Skill |
|---------------------|-------|
| "I want to learn RAG" / "Where should I start?" | `learning-path-advisor` |
| "Explain attention" / "Quiz me on agents" | `ai-tutor` |
| "I have 2 hours — coach my session" | `study-session-coach` |
| "Interview me on RAG system design" | `mock-interviewer` |

Full guide: [docs/learn/using-tutor-skills.md](docs/learn/using-tutor-skills.md)

**Universal Agent Guide:** `AGENTS.md`  
**Routing reference:** `.claude/references/handbook-routing.md`

## For contributors (author skills)

| Skill | Purpose |
|-------|---------|
| `curriculum-content-writer` | Add/edit handbook lessons |
| `interview-question-writer` | Add interview Q&A pages |
| `system-design-case-study-writer` | Add system design case studies |

## Site navigation

```
curriculum.yml  →  npm run sync-nav  →  mkdocs.yml
```

Do not hand-edit `nav:` in `mkdocs.yml`. See `CONTRIBUTING.md` and `DEPTH_STANDARDS.md`.

## Build docs locally

```bash
pip install -r requirements.txt
npm install
npm run sync-nav
mkdocs serve
```

## Key entry points

- `docs/start-here.md` — pick a path by background
- `docs/learn/index.md` — 16 courses in order
- `docs/learn/study-plans.md` — week-by-week schedules
- `docs/topic-map.md` — find any concept
