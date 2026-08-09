# Contributing to AI Engineering Handbook

Thank you for helping grow this open knowledge base.

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before participating.

## Ways to contribute

1. **Fix a lesson** — typos, clearer explanations, updated code samples
2. **Add a resource** — papers, videos, or tools in `resources/`
3. **Add an exercise** — `exercises/*-starter.py` + `*-solution.py` in a module folder
4. **Add a notebook** — `.ipynb` alongside an exercise for interactive learning
5. **Fill content gaps** — see module READMEs with incomplete lesson counts

## Lesson frontmatter

```yaml
---
title: "Your Lesson Title"
description: "One-line summary"
duration: "30 min"
difficulty: beginner   # beginner | intermediate | advanced
has_code: false
youtube: "https://..."  # optional
objectives:           # optional
  - "What the learner will know"
---
```

## File layout

```text
docs/
  {phase}/                         # foundations | build | production | advanced
    index.md                       # phase overview
    module-{NN}-{slug}/
      index.md                     # module overview + lesson table
      lessons/
        01-lesson-slug.md
      exercises/                   # optional
        01-starter.py
        01-solution.py
```

## Code fences — always label the language

Every fence must declare a language, even for ASCII diagrams and program output:

- Runnable code: ` ```python `, ` ```bash `, ` ```json `, ` ```yaml `, etc.
- ASCII diagrams, tree layouts, math derivations, or console/program output: ` ```text `
- Architecture diagrams that can be drawn as a graph: prefer ` ```mermaid ` over ASCII art — it renders as an actual diagram and stays readable on mobile.

An unlabeled fence (bare ` ``` `) fails CI. Run the linter locally before opening a PR:

```bash
npm run lint:fences
```

The allowed language list lives in `scripts/lint-code-fences.mjs` — add to it if you have a genuine new case (e.g. `rust`, `go`), don't just silence the error.

## Reusable snippets

Content repeated across multiple pages (setup instructions, standard admonitions, disclaimers) belongs in `docs/_snippets/` and is pulled in with:

```markdown
--8<-- "snippet-name.md"
```

Existing snippets:

| Snippet | Use for |
|---|---|
| `scaffold-note.md` | Marking a page as a work-in-progress scaffold, with a link to good-first-issues |
| `api-key-setup.md` | Standard "install the SDK + export your API key" callout before a runnable example |

To add a new one: create `docs/_snippets/your-snippet.md`, then reference it from any page with `--8<-- "your-snippet.md"`. `pymdownx.snippets` is configured with `check_paths: true`, so a typo'd snippet name fails the build immediately rather than silently rendering nothing.

Module IDs (`module-00`, `module-09`, etc.) match the AI Engineering Mastery platform on disk. **Site navigation** uses numbered course titles from `curriculum.yml` — run `npm run sync-nav` after changing order or adding courses. See [MAINTAINING.md](../maintainers/MAINTAINING.md).

## Site navigation

```
curriculum.yml  →  npm run sync-nav  →  mkdocs.yml + learn/index.md
```

Do not hand-edit the `nav:` section of `mkdocs.yml`.

**Important:** Raw HTML links in markdown (`<a href="page.md">`) break on GitHub Pages. Use trailing-slash paths (`href="page/"`) in HTML blocks, or markdown links `[text](page.md)`. The build runs `scripts/fix-site-links.mjs` as a safety net.

## Pull request checklist

- [ ] Markdown renders correctly (`mkdocs serve` locally)
- [ ] Links work (no broken URLs where you can help it)
- [ ] Original writing or properly attributed quotes
- [ ] No secrets, API keys, or `.env` files
- [ ] Python exercises run with stated dependencies

## Content gaps (known)

- **Multi-Agent Systems** — partial module; more lessons planned
- **Notebooks** — being added module by module
- **Central bibliography** — run `npm run extract-resources` to refresh link indexes

## Code of conduct

Be constructive, cite sources, and optimize for learners at different levels.
