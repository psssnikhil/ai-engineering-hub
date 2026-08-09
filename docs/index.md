---
title: "AI Engineering Hub — The All-in-One Destination for AI Learning, Labs, Resources & Interview Prep"
description: "The definitive open-source AI Engineering hub: 16 sequential courses, 30+ executable labs, 10 portfolio projects, system design interview prep, and curated AI research resources."
keywords: "AI engineering, RAG tutorial, AI agents, LLMOps, AI course, fine-tuning, transformers, LLM evaluation, system design interview prep, open source AI curriculum"
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
  <div class="hero__badge">✨ The Go-To Open-Source AI Engineering Hub</div>
  <p class="hero__tagline">The All-in-One Destination for AI Learning, Labs, Resources &amp; Interview Prep</p>
  <p class="hero__sub">One unified open-source platform. From PyTorch &amp; Transformer math to Hybrid RAG, Autonomous AI Agents, System Design Interviews, and Production LLMOps. 100% Free. Real production code.</p>
  <div class="hero__actions">
    <a class="hero__btn hero__btn--primary" href="start-here/">⚡ Start Here</a>
    <a class="hero__btn hero__btn--secondary" href="learn/">📚 Browse 16 Courses</a>
    <a class="hero__btn hero__btn--github" href="https://github.com/psssnikhil/ai-engineering-hub">★ Star on GitHub</a>
  </div>

  <div class="tutor-prompt-bar" style="margin-top: 1.8rem; background: rgba(255, 255, 255, 0.4);">
    <span class="tutor-prompt-bar__label">🤖 IDE AI Tutor Prompts:</span>
    <span class="tutor-chip">"Where should I start?"</span>
    <span class="tutor-chip">"Explain scaled dot-product attention"</span>
    <span class="tutor-chip">"Mock interview: RAG system design"</span>
    <span class="tutor-chip">"Review my agent loop"</span>
  </div>
</div>

<div class="stat-row">
  <span class="stat-pill"><span class="stat-pill__dot"></span><span class="stat-pill__value">16</span> Core Courses</span>
  <span class="stat-pill"><span class="stat-pill__dot"></span><span class="stat-pill__value">140+</span> Lessons</span>
  <span class="stat-pill"><span class="stat-pill__dot"></span><span class="stat-pill__value">3</span> Specialized Tracks</span>
  <span class="stat-pill"><span class="stat-pill__dot"></span><span class="stat-pill__value">30+</span> Executable Labs</span>
  <span class="stat-pill"><span class="stat-pill__dot"></span><span class="stat-pill__value">100%</span> Open Source</span>
</div>

---

## 🌟 The 5 Pillars: Everything You Need in One Hub

Why look across dozens of scattered blogs, paid bootcamps, and disconnected repos? This repository unifies the complete AI engineering stack:

<div class="persona-grid">
  <div class="persona-card">
    <div class="persona-card__icon">📚</div>
    <div class="persona-card__title">1. Complete Learning Path</div>
    <div class="persona-card__desc">16 sequential, deep-dive courses from tokenization math &amp; attention to LoRA fine-tuning, vLLM serving, and enterprise capstones.</div>
    <a class="persona-card__cta" href="learn/">Explore 16 Courses →</a>
  </div>

  <div class="persona-card">
    <div class="persona-card__icon">🛠️</div>
    <div class="persona-card__title">2. Executable Labs &amp; Projects</div>
    <div class="persona-card__desc">30+ hands-on Python labs and 10 portfolio projects with starter code and verified solutions: Doc Q&amp;A, Tool Agents, Hybrid Vector Search, and Guardrails.</div>
    <a class="persona-card__cta" href="projects/build-these/">Build Projects →</a>
  </div>

  <div class="persona-card">
    <div class="persona-card__icon">💼</div>
    <div class="persona-card__title">3. Interview Prep &amp; System Design</div>
    <div class="persona-card__desc">Land Senior AI roles with 10 full 45-minute whiteboard case studies (RAG, Agent Platforms, LLM Serving) and 50+ detailed technical question banks.</div>
    <a class="persona-card__cta" href="interview-prep/">Interview Track →</a>
  </div>

  <div class="persona-card">
    <div class="persona-card__icon">📖</div>
    <div class="persona-card__title">4. Curated Papers &amp; Resources</div>
    <div class="persona-card__desc">Seminal research papers, open-source repositories, free video masterclasses, and topic deep dives organized by domain.</div>
    <a class="persona-card__cta" href="resources/">Curated Resources →</a>
  </div>

  <div class="persona-card">
    <div class="persona-card__icon">🤖</div>
    <div class="persona-card__title">5. Interactive Socratic IDE Tutoring</div>
    <div class="persona-card__desc">Clone the repo and pair-program in your IDE (Claude Code, Cursor, Antigravity) using built-in AI tutor skills and automated lab verifiers.</div>
    <a class="persona-card__cta" href="ai-engineering-2026/">Modern AI (2026) →</a>
  </div>
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

## 🧭 Navigation & Shortcuts

<div class="quick-nav">
  <a class="quick-nav__item" href="start-here/">🚀 Start Here</a>
  <a class="quick-nav__item" href="learn/">📚 Learn Courses</a>
  <a class="quick-nav__item" href="learn/study-plans/">⏱️ Study Plans</a>
  <a class="quick-nav__item" href="projects/build-these/">🛠️ Build Projects</a>
  <a class="quick-nav__item" href="topic-map/">🗺️ Topic Map</a>
  <a class="quick-nav__item" href="faq/">💡 FAQ</a>
  <a class="quick-nav__item" href="getting-started/">⚙️ Setup</a>
</div>

| Goal | Destination |
|------|-------------|
| **Follow the curriculum** | **[Learn](learn/index.md)** — 16 courses in order |
| **New here** | [Start Here](start-here.md) |
| **Week-by-week schedule** | [Study Plans](learn/study-plans.md) |
| **Build a portfolio** | [Build These First](projects/build-these.md) |
| **Find any topic** | [Topic Map](topic-map.md) |
| **Questions** | [FAQ](faq.md) |

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

## 👨‍💻 Connect with Author & Community

This open handbook is maintained by **[Nikhil Pentapalli](https://www.linkedin.com/in/nikhilpentapalli/)** and open-source contributors.

- 💼 **Connect on LinkedIn**: Follow or reach out at **[linkedin.com/in/nikhilpentapalli](https://www.linkedin.com/in/nikhilpentapalli/)**.
- 🎯 **1:1 Mentorship & System Design**: Book a session on **[Topmate](https://topmate.io/nikhil_pentapalli)**.
- 🏢 **Enterprise AI Consulting**: For enterprise AI systems design, team training, or advisory, email **[psss.nikhil@gmail.com](mailto:psss.nikhil@gmail.com)**.
- ⭐️ **Support Open Source**: If this repository helps you learn or ship AI systems, **[star the repository on GitHub](https://github.com/psssnikhil/ai-engineering-hub)**!

[Contribute Guide](contribute.md) · [Roadmap](roadmap.md)
