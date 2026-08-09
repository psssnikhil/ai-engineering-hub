## Summary

<!-- Provide a brief, high-level summary of what this PR introduces or fixes. -->

| Type of Change | Check |
|----------------|:-----:|
| 📖 Curriculum / Handbook Lesson | [ ] |
| 🧪 New Executable Lab Notebook | [ ] |
| 🤖 Agent Skill / Rule Update | [ ] |
| 💼 Interview Prep / Case Study | [ ] |
| 🛠 Tooling / Script / CI/CD Fix | [ ] |

---

## What Changes Were Made?

<!-- Bulleted list of specific changes, new files added, or modifications made. -->
- 

---

## Test Plan & Verification

Please ensure all appropriate verification checks pass before requesting review:

- [ ] `npm run sync-nav` — Synced navigation (`curriculum.yml` → `mkdocs.yml`)
- [ ] `mkdocs build --strict` — Site builds locally with **0 errors or broken links**
- [ ] `node scripts/verify-site-links.mjs` — All internal and external links verified
- [ ] Runnable code / notebook verified without errors (if applicable)

```bash
# Verification commands run locally:
npm run sync-nav
mkdocs build --strict
```

---

## Checklist

- [ ] Follows the handbook's [DEPTH_STANDARDS.md](maintainers/DEPTH_STANDARDS.md) content bar.
- [ ] Preserves LaTeX math syntax (`\( ... \)` for inline, `\[ ... \]` for block).
- [ ] No raw secret keys committed.
