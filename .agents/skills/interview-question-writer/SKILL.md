---
name: interview-question-writer
description: Use when adding or extending AI/ML engineer interview question pages (docs/interview-prep/questions-*.md or similar). Produces question-answer content that teaches, not just quizzes — every answer explains the reasoning, not just the correct choice, matching this repo's DEPTH_STANDARDS.md bar.
---

# Interview question writer

Companion to `curriculum-content-writer` — read that first for repo wiring
(`curriculum.yml` → `npm run sync-nav`) and frontmatter rules. This skill is specific to
writing **interview Q&A content** under `docs/interview-prep/`.

## What makes a good entry here

A weak interview page is a list of questions with one-line answers — that's a quiz, not
a lesson, and DEPTH_STANDARDS.md explicitly bans "bullet lists without explanation."

A good entry:

1. **States the question** the way an interviewer would actually ask it — including
   follow-up pressure ("why not just increase the learning rate?").
2. **Gives the model answer** with reasoning, not just the conclusion — a candidate who
   memorizes the conclusion fails the follow-up.
3. **Names the follow-up question** an interviewer is likely to ask next, and answers
   that too, one level deeper.
4. **Flags the common wrong answer** — what a junior candidate says, and why it's
   incomplete or wrong.
5. Links back to the relevant lesson in the main curriculum for readers who need the
   fundamentals first (e.g. a transformer question links to
   `foundations/module-06-transformers-attention-mechanisms`).

## Format template

```markdown
### Q: <question as asked>

**Short answer:** <1-2 sentence answer a strong candidate gives first>

<2-4 paragraphs of the full reasoning, worked example, or numbers where relevant>

**Likely follow-up:** <next question> — <answer>

!!! warning "Common wrong answer"
    <what weaker candidates say and why it falls short>

*See also: [<lesson title>](<relative link>)*
```

## Grouping

Group questions by topic (transformers/LLM fundamentals, RAG, agents, evals/production,
behavioral/ML-generalist), one file per topic, 6-10 questions per file — not one giant
page. This keeps each page a focused study session rather than a wall of text.

## Difficulty labeling

Tag each question inline with `L1` (screening), `L2` (mid-level), `L3` (senior/staff) so
readers can filter by the level they're prepping for. Mix levels within a topic file
rather than splitting files by level — real interview loops mix difficulty too.
