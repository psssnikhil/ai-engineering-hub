---
title: "07. AI Agents Fundamentals"
phase: Build
module_id: module-11
---

# 07. AI Agents Fundamentals

Master AI agents from ground zero: reasoning loops (ReAct), tool integration, memory architectures, multi-step planning, state management, and modern agent frameworks.

<div class="lesson-meta">
  <span class="badge badge--module">Course 07</span>
  <span class="badge badge--intermediate">⚡ Intermediate → Advanced</span>
  <span class="badge">⏱️ 10 lessons · ~16h</span>
</div>

---

## 🤖 Cognitive Agent Execution Loop Architecture

```mermaid
flowchart TD
    classDef user fill:#eef2ff,stroke:#6366f1,stroke-width:2px;
    classDef core fill:#f5f3ff,stroke:#8b5cf6,stroke-width:2px;
    classDef mem fill:#fff7ed,stroke:#f59e0b,stroke-width:2px;
    classDef tools fill:#f0fdf4,stroke:#10b981,stroke-width:2px;

    UserGoal["User Request / Goal Specification"]:::user --> ReActLoop["Agent Core Loop (LLM)"]:::core
    
    subgraph CognitiveLoop["Reasoning & Acting Loop"]
        ReActLoop --> Thought["1. Thought (Analyze Goal & Memory)"]:::core
        Thought --> Decision{"Tool Call Needed?"}:::core
        
        Decision -- Yes --> ToolCall["2. Action (Format Tool Parameters)"]:::tools
        ToolCall --> Execution["3. Tool Execution (API / Web / Code Sandbox)"]:::tools
        Execution --> Observation["4. Observation (Parse Result)"]:::tools
        Observation --> ReActLoop
        
        Decision -- No --> FinalAns["5. Final Answer Generation"]:::user
    end

    subgraph MemoryLayer["Context & Memory Layer"]
        ShortTerm["Short-term History (Window)"]:::mem <--> ReActLoop
        LongTerm[("Long-term Memory (Vector Store)")]:::mem <--> ReActLoop
    end
```

---

## 📚 Course Lessons

| # | Lesson Title | Duration | Level | Core Concept |
|---|--------------|----------|-------|--------------|
| 1 | [Introduction to AI Agents](lessons/01-Introduction-to-Agents.md) | 60 min | <span class="badge badge--intermediate">⚡ Intermediate</span> | Definition, agent vs workflow, autonomy spectrum |
| 2 | [Agent Architectures](lessons/02-Agent-Architectures.md) | 60 min | <span class="badge badge--advanced">🔥 Advanced</span> | ReAct, Plan-and-Solve, Reflection, LATS (Language Agent Tree Search) |
| 3 | [The ReAct Pattern — Reasoning & Acting](lessons/03-ReAct-Pattern.md) | 65 min | <span class="badge badge--advanced">🔥 Advanced</span> | Deconstructing Thought-Action-Observation loops step-by-step |
| 4 | [Tool Use & Function Calling](lessons/04-Tool-Use.md) | 60 min | <span class="badge badge--advanced">🔥 Advanced</span> | Schema design, tool parameter validation, handling execution errors |
| 5 | [Agent Memory Systems](lessons/05-Agent-Memory.md) | 60 min | <span class="badge badge--advanced">🔥 Advanced</span> | Short-term conversation buffer, semantic long-term memory, procedural memory |
| 6 | [Planning & Reasoning](lessons/06-Planning-and-Reasoning.md) | 35 min | <span class="badge badge--advanced">🔥 Advanced</span> | Task decomposition, sub-goal generation, self-correction |
| 7 | [Building an Agent from Scratch](lessons/07-Building-an-Agent.md) | 45 min | <span class="badge badge--advanced">🔥 Advanced</span> | Pure Python zero-dependency ReAct agent implementation |
| 8 | [Agent Frameworks (LangGraph, CrewAI)](lessons/08-Agent-Frameworks.md) | 35 min | <span class="badge badge--advanced">🔥 Advanced</span> | State graphs, persistence, streaming, multi-agent frameworks |
| 9 | [Agent Types & Patterns](lessons/09-Agent-Types.md) | 35 min | <span class="badge badge--advanced">🔥 Advanced</span> | Research agents, coding agents, customer support agents |
| 10 | [Workflow vs Agent Design](lessons/10-Workflow-vs-Agent.md) | 35 min | <span class="badge badge--advanced">🔥 Advanced</span> | Deterministic DAG vs autonomous agent decision matrix |

---

👉 **Get Started:** [Lesson 01 · Introduction to AI Agents](lessons/01-Introduction-to-Agents.md)
