---
title: Contribute
---

<div class="top-launcher">
  <div class="hero__badge">🤝 Open Source Community</div>
  <h1 class="top-launcher__title">Contribute &amp; Build the #1 AI Engineering Resource</h1>
  <p class="top-launcher__subtitle">The AI Engineering Hub is 100% MIT-licensed and community-driven. Help us expand lessons, build code labs, polish math explanations, and add system design case studies!</p>

  <div class="filter-chips">
    <a class="chip-btn chip-btn--active" href="#quick-wins">⚡ Quick Wins</a>
    <a class="chip-btn" href="#content-standards">📋 Content Standards</a>
    <a class="chip-btn" href="#local-preview">⚙️ Local Preview</a>
    <a class="chip-btn" href="#adding-a-course-to-the-curriculum">📚 Add a Lesson/Course</a>
    <a class="chip-btn" href="https://github.com/psssnikhil/ai-engineering-hub">★ Star Repository</a>
  </div>
</div>

<div class="spotlight-grid">
  <div class="spotlight-card">
    <span class="spotlight-card__tag">⚡ 5-Minute Contribution</span>
    <h3 class="spotlight-card__title">Fix Typos &amp; Diagrams</h3>
    <p class="spotlight-card__desc">Spotted a typo or broken link? Submit a quick PR directly on GitHub.</p>
    <a class="persona-card__cta" href="https://github.com/psssnikhil/ai-engineering-hub/issues/new/choose">Open an Issue →</a>
  </div>
  <div class="spotlight-card">
    <span class="spotlight-card__tag">🐍 Python Labs</span>
    <h3 class="spotlight-card__title">Add Exercises &amp; Labs</h3>
    <p class="spotlight-card__desc">Add executable starter code and solution scripts for curriculum modules.</p>
    <a class="persona-card__cta" href="#adding-a-course-to-the-curriculum">Lab Guidelines →</a>
  </div>
  <div class="spotlight-card">
    <span class="spotlight-card__tag">📚 Content Writing</span>
    <h3 class="spotlight-card__title">Write System Design Cases</h3>
    <p class="spotlight-card__desc">Expand our 45-minute whiteboard case studies and technical interview Q&amp;As.</p>
    <a class="persona-card__cta" href="#content-standards">Content Bar Standard →</a>
  </div>
</div>

## Quick wins

| Type | How |
|------|-----|
| **Fix a lesson** | Edit markdown in `docs/`, open a PR |
| **Fix a broken link** | Use trailing-slash paths in HTML (`href="page/"`), not `.md` |
| **Add an exercise** | `exercises/*-starter.py` + solution in a course folder |
| **Report a gap** | [Open an issue](https://github.com/psssnikhil/ai-engineering-hub/issues/new/choose) |

## Content standards

1. **Frontmatter** — `title`, `description`, `duration`, `difficulty`
2. **Structure** — objectives → content → key takeaways → next lesson
3. **Code** — Python 3.10+, runnable where `has_code: true`
4. **Tone** — learner-facing only (no author meta, word counts, or internal standards on pages)
5. **Links** — markdown links OK; raw HTML must use `href="path/"` not `href="path.md"`

## Local preview

```bash
pip install -r requirements.txt
npm install
mkdocs serve          # preview
npm run build:docs    # full build + link fix (same as CI)
```

## Adding a course to the curriculum

1. Add content under `docs/{phase}/module-NN-{slug}/`
2. Edit `curriculum.yml` in order
3. Run `npm run sync-nav`

See [MAINTAINING.md](https://github.com/psssnikhil/ai-engineering-hub/blob/main/maintainers/MAINTAINING.md) for curriculum structure details.

Full guide: [CONTRIBUTING.md](https://github.com/psssnikhil/ai-engineering-hub/blob/main/.github/CONTRIBUTING.md)
