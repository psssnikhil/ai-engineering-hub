---
name: curriculum-content-writer
description: Use whenever adding or editing a lesson, track page, or hub page in this repo (docs/**). Encodes the repo's structure rules (curriculum.yml → npm run sync-nav → mkdocs.yml), frontmatter format, and the DEPTH_STANDARDS.md content bar, so generated pages match the rest of the handbook without a manual review pass.
---

# Curriculum content writer

This repo is a sequential AI engineering handbook built with MkDocs. Content lives in
`docs/`, but **navigation is generated, not hand-written** — never edit the `nav:` block
in `mkdocs.yml` directly.

## Before writing anything

1. Read `DEPTH_STANDARDS.md` — structure, depth targets, math formatting, anti-patterns.
2. Read `curriculum.yml` — decide whether new content is a **course** (sequential 01-16
   path), a **track** (focused, optional, `tracks:` list with `pages:`), or a
   **reference** entry (`reference:` list, single page).
3. Look at one existing sibling page in the same section for exact tone/format before
   writing new ones (e.g. `docs/agent-engineering/01-agent-loop.md` for a track page).

## Frontmatter (every page)

```yaml
---
title: "Page Title"
description: "One-line summary"
---
```

Lesson pages inside numbered courses may add `duration`, `difficulty`, `has_code`,
`objectives` — see `CONTRIBUTING.md` → "Lesson frontmatter". Track pages typically just
use `title` + `description`.

## Structure to follow (from DEPTH_STANDARDS.md)

Prerequisites → What You'll Learn (objectives table) → Intuition first → Core theory →
Worked example → Implementation (if code) → Edge cases & misconceptions → Production
connection → Key takeaways (5-8 bullets) → Further reading → Next lesson link.

Not every page needs all sections (a Q&A or case-study page can adapt this loosely), but
**intuition-first, then depth, then a takeaways list** is the non-negotiable shape.

## Math and links

- Math: `\( ... \)` inline, `\[ ... \]` block. Never bare `$...$` (breaks on dollar
  amounts like `$0.04`).
- Cross-links: markdown links `[text](../path/to/page.md)`, not raw `<a href>` (breaks
  on GitHub Pages unless using trailing-slash `page/` form).
- Diagrams: mermaid fenced blocks, used sparingly (1-4 per page) and only when they add
  structure a table/prose can't.

## Wiring a new page into the site

1. Write the `.md` file under `docs/<section>/`.
2. Add an entry to `curriculum.yml`:
   - New course → append to `courses:` in sequence order.
   - New track → append to `tracks:`, with a `pages:` list of `{ title, file }`.
   - Standalone reference page → append to `reference:`.
3. Run `npm run sync-nav` — regenerates `mkdocs.yml` nav and `docs/learn/index.md`'s
   course table from `curriculum.yml`. Do this after every structural change.
4. If possible, sanity-check with `mkdocs build --strict` (or at minimum confirm
   `curriculum.yml` still parses as YAML and `mkdocs.yml` nav updated as expected) —
   the full `npm run build:docs` also runs link verification.

## Anti-patterns to avoid (from DEPTH_STANDARDS.md)

Marketing fluff, unexplained bullet lists, "see docs" non-answers, salary tables,
decorative stock imagery. Prefer worked numerical examples, "why not X" comparisons,
and tensor shape annotations over abstract prose.
