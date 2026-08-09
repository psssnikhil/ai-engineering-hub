## 📌 PR Summary & Context

<!-- Provide a brief, high-level summary of what this PR introduces or fixes. -->

- **Related Issue**: Fixes # <!-- e.g. #8 -->
- **Type of Change**:
  - [ ] 📖 Curriculum / Handbook Lesson
  - [ ] 🧪 New Executable Lab Notebook
  - [ ] 🤖 Agent Skill / Rule Update
  - [ ] 💼 Interview Prep / Case Study
  - [ ] 🛠 Tooling / Script / CI/CD Fix

---

## 🤖 AI Agent Pre-Flight Checklist

> **If this PR was generated or assisted by an AI agent (Claude Code, Cursor, Antigravity, Windsurf, Aider, etc.), the following rules MUST be verified before opening:**

- [ ] **Nav Sync**: Updated `curriculum.yml` and ran `npm run sync-nav` (did **NOT** manually edit `nav:` block in `mkdocs.yml`).
- [ ] **Strict Build**: Ran `npm run build:docs` (`mkdocs build --strict`) with **0 errors, warnings, or broken links**.
- [ ] **Code Labs Quality**: If editing/adding notebooks in `labs/`, verified zero framework bloat, explicit error handling/fallbacks, and saved cell outputs.
- [ ] **LaTeX Math**: Preserved standard math delimiters (`\( ... \)` for inline, `\[ ... \]` for block).
- [ ] **Secrets & Security**: Verified **no API keys, tokens, or raw secrets** are committed.

---

## 👤 Human Contributor Checklist

- [ ] I have read the [CONTRIBUTING.md](.github/CONTRIBUTING.md) and content guidelines in `maintainers/DEPTH_STANDARDS.md`.
- [ ] My changes are focused, clear, and accurately documented.
- [ ] All internal markdown file links use standard github-style links and resolve cleanly.
- [ ] I have tested code snippets locally to ensure they execute without errors.

---

## 🧪 Verification Log Output

Paste terminal output from `npm run build:docs` below to prove validation:

```bash
# Example output from npm run build:docs:
# INFO - Building documentation to directory: .../site
# INFO - Documentation built in 4.25 seconds
# OK: 6 required pages, no internal .md hrefs
```
