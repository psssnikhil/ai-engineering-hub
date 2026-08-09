---
title: "AI Engineering Hub — Free Open Source AI Engineering Course & Roadmap"
description: "Master AI Engineering from ground zero to production: Transformers, RAG, Autonomous AI Agents, LLMOps, Evals, and Fine-Tuning. Free open-source curriculum."
keywords: "AI engineering, RAG tutorial, AI agents, LLMOps, AI course, fine-tuning, transformers, LLM evaluation, open source AI curriculum"
hide:
  - navigation
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Course",
  "name": "AI Engineering Hub",
  "description": "The free, open-source path from transformers to production AI — RAG, agents, harnesses, evals, and LLMOps.",
  "provider": {
    "@type": "Organization",
    "name": "AI Engineering Hub Contributors",
    "sameAs": "https://github.com/psssnikhil/ai-engineering-hub"
  },
  "educationalCredentialAwarded": "Open Source AI Engineering Mastery",
  "hasCourseInstance": {
    "@type": "CourseInstance",
    "courseMode": "online",
    "courseWorkload": "PT40H"
  }
}
</script>

# AI Engineering Hub

<div class="hero">
  <div class="hero__badge">Free &amp; Open Source</div>
  <p class="hero__tagline">The path from transformers to production AI</p>
  <p class="hero__sub">One sequential curriculum — transformers, RAG, agents, harnesses, evals, and LLMOps. No scattered tutorials. Just start at course 01 and build real systems.</p>
  <div class="hero__actions">
    <a class="hero__btn hero__btn--primary" href="start-here/">Start Here</a>
    <a class="hero__btn hero__btn--secondary" href="learn/">Browse 16 Courses</a>
    <a class="hero__btn hero__btn--github" href="https://github.com/psssnikhil/ai-engineering-hub">★ Star on GitHub</a>
  </div>
</div>

<div class="stat-row">
  <span class="stat-pill"><span class="stat-pill__dot"></span><span class="stat-pill__value">16</span> Courses</span>
  <span class="stat-pill"><span class="stat-pill__dot"></span><span class="stat-pill__value">140+</span> Lessons</span>
  <span class="stat-pill"><span class="stat-pill__dot"></span><span class="stat-pill__value">3</span> Specialized Tracks</span>
  <span class="stat-pill"><span class="stat-pill__dot"></span><span class="stat-pill__value">30+</span> Hands-on Labs</span>
  <span class="stat-pill"><span class="stat-pill__dot"></span><span class="stat-pill__value">MIT</span> License</span>
</div>

---

## Quick start path

<div class="phase-stepper">
  <a class="phase-step" href="start-here/">
    <span class="phase-step__num">1</span>
    <span class="phase-step__info">
      <span class="phase-step__title">Start Here</span>
      <span class="phase-step__sub">Pick a path by background</span>
    </span>
  </a>
  <a class="phase-step" href="learn/">
    <span class="phase-step__num">2</span>
    <span class="phase-step__info">
      <span class="phase-step__title">Browse Courses</span>
      <span class="phase-step__sub">16 courses, sequential order</span>
    </span>
  </a>
  <a class="phase-step" href="learn/study-plans/">
    <span class="phase-step__num">3</span>
    <span class="phase-step__info">
      <span class="phase-step__title">Study Plans</span>
      <span class="phase-step__sub">Week-by-week schedule</span>
    </span>
  </a>
  <a class="phase-step" href="projects/build-these/">
    <span class="phase-step__num">4</span>
    <span class="phase-step__info">
      <span class="phase-step__title">Build Projects</span>
      <span class="phase-step__sub">Ship a portfolio piece</span>
    </span>
  </a>
</div>

---

## 🗺️ Curriculum Architecture

```mermaid
flowchart TD
    classDef foundation fill:#eef2ff,stroke:#6366f1,stroke-width:2px,color:#312e81;
    classDef build fill:#f0fdf4,stroke:#10b981,stroke-width:2px,color:#064e3b;
    classDef prod fill:#fff7ed,stroke:#f59e0b,stroke-width:2px,color:#78350f;
    classDef adv fill:#fdf2f8,stroke:#f43f5e,stroke-width:2px,color:#881337;
    classDef track fill:#f5f3ff,stroke:#8b5cf6,stroke-width:2px,color:#4c1d95;

    subgraph Phase1["1. Understand AI (Courses 01–05)"]
        C01["01. GenAI Foundations"]:::foundation --> C02["02. AI Essentials"]:::foundation
        C02 --> C03["03. Neural Networks"]:::foundation
        C03 --> C04["04. Transformers & Attention"]:::foundation
        C04 --> C05["05. Large Language Models"]:::foundation
    end

    subgraph Phase2["2. Build Systems (Courses 06–11)"]
        C05 --> C06["06. RAG Systems"]:::build
        C06 --> C07["07. AI Agents"]:::build
        C07 --> C08["08. Agent Harness & Runtime"]:::build
        C08 --> C09["09. Multi-Agent Systems"]:::build
        C06 --> C10["10. Vector Databases"]:::build
        C07 --> C11["11. Prompt Mastery"]:::build
    end

    subgraph Phase3["3. Production & Scale (Courses 12–14)"]
        C09 --> C12["12. LLMOps & Serving"]:::prod
        C12 --> C13["13. LLM Evals & Quality"]:::prod
        C13 --> C14["14. AI Safety & Guardrails"]:::prod
    end

    subgraph Phase4["4. Advanced & Capstones (Courses 15–16)"]
        C14 --> C15["15. Fine-Tuning & Quantization"]:::adv
        C15 --> C16["16. Enterprise Capstone Projects"]:::adv
    end

    subgraph Tracks["Specialized Role Tracks"]
        T1["Track 1: Agent Engineering"]:::track
        T2["Track 2: Interview Prep & System Design"]:::track
        T3["Track 3: Modern AI & IDE Agents (2026)"]:::track
    end

    C07 -.-> T1
    C12 -.-> T2
    C08 -.-> T3
```

---

## 🎯 Who is this for?

<div class="persona-grid">
  <div class="persona-card">
    <div class="persona-card__icon">🌱</div>
    <div class="persona-card__title">New to AI</div>
    <div class="persona-card__desc">Software engineer or student starting from ground zero with Python and LLMs.</div>
    <a class="persona-card__cta" href="start-here/">Start Here →</a>
  </div>
  <div class="persona-card">
    <div class="persona-card__icon">🧠</div>
    <div class="persona-card__title">Know ML, need LLMs</div>
    <div class="persona-card__desc">ML practitioner catching up on modern transformers, APIs, vector DBs, and fine-tuning.</div>
    <a class="persona-card__cta" href="learn/">Browse Curriculum →</a>
  </div>
  <div class="persona-card">
    <div class="persona-card__icon">🤖</div>
    <div class="persona-card__title">Building AI Agents</div>
    <div class="persona-card__desc">Engineer shipping autonomous agent loops, tools, MCP, and multi-agent systems.</div>
    <a class="persona-card__cta" href="agent-engineering/">Agent Track →</a>
  </div>
  <div class="persona-card">
    <div class="persona-card__icon">⚡</div>
    <div class="persona-card__title">IDE &amp; Coding Agents</div>
    <div class="persona-card__desc">Mastering Claude Code, Cursor skills, execution loops, and context engineering.</div>
    <a class="persona-card__cta" href="ai-engineering-2026/">Modern AI (2026) →</a>
  </div>
  <div class="persona-card">
    <div class="persona-card__icon">🛡️</div>
    <div class="persona-card__title">Shipping to Production</div>
    <div class="persona-card__desc">Architecting LLMOps, automated evals, continuous monitoring, and security guardrails.</div>
    <a class="persona-card__cta" href="production/module-10-llmops-production-systems/">Production Track →</a>
  </div>
</div>

---

## More shortcuts

<div class="quick-nav">
  <a class="quick-nav__item" href="topic-map/">Topic Map</a>
  <a class="quick-nav__item" href="faq/">FAQ</a>
  <a class="quick-nav__item" href="getting-started/">Setup</a>
</div>

---

## ⚡ The Learning Roadmap

| Stage | Courses | Core Topics Covered |
|-------|---------|--------------------|
| **1. Understand AI** | 01–05 | NLP → neural nets → transformers → attention → LLM architecture |
| **2. Build Applications** | 06–11 | Modular RAG, autonomous agents, tool runtime, multi-agent systems, vector DBs, prompts |
| **3. Production & Ops** | 12–14 | Serving, vLLM/Ollama, LLMOps, automated evals, safety & guardrail gateways |
| **4. Advanced** | 15–16 | Fine-tuning (LoRA/QLoRA), quantization, enterprise capstones |

Specialized tracks: [Agent Engineering](agent-engineering/index.md) · [Interview Prep & System Design](interview-prep/index.md) · [Modern AI (2026)](ai-engineering-2026/index.md)

---

## 🤝 Contribute & Star

If this open handbook helps you learn or ship AI systems, **[star the repository on GitHub](https://github.com/psssnikhil/ai-engineering-hub)** to support open AI education.

Improve a lesson, fix a link, or submit an exercise: [Contribute Guide](contribute.md) · [Roadmap](roadmap.md)

