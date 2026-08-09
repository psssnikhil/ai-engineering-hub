---
title: Topic Resources — AI Agents & Harness Engineering
description: Curated papers, open-source repositories, YouTube lectures, free courses, and code references for AI Agents, Model Context Protocol (MCP), and Multi-Agent Orchestration.
---

# 🤖 AI Agents & Harness Engineering — Topic Resources

Curated list of top landmark papers, open-source repositories, video series, free courses, and code references for **AI Agents, Agent Harnesses, Model Context Protocol (MCP), Tool Execution, Memory Systems, and Multi-Agent Systems**.

---

## 📄 Landmark Papers & Essential Reading

| Paper / Reference | Key Takeaways & Focus | Link |
|-------------------|-----------------------|------|
| **ReAct: Synergizing Reasoning and Acting in Language Models** *(Yao et al., 2022)* | Introduced the interleaved Thought-Action-Observation loop driving modern autonomous agents. | [ArXiv Link](https://arxiv.org/abs/2210.03629) |
| **Toolformer: Language Models Can Teach Themselves to Use Tools** *(Schick et al., 2023)* | Showed self-supervised training for LLMs to invoke APIs dynamically via specialized token calls. | [ArXiv Link](https://arxiv.org/abs/2302.04761) |
| **Generative Agents: Interactive Simulacra of Human Behavior** *(Park et al., 2023)* | Landmark paper detailing architectural memory stream, reflection, and planning for multi-agent social simulations. | [ArXiv Link](https://arxiv.org/abs/2304.03442) |
| **Reflexion: Language Agents with Verbal Reinforcement Learning** *(Shinn et al., 2023)* | Autonomous agents reflecting on execution feedback, storing verbal memories to avoid repeating mistakes. | [ArXiv Link](https://arxiv.org/abs/2303.11366) |
| **Voyager: An Open-Ended Embodied Agent with Large Language Models** *(Wang et al., 2023)* | Showed lifelong learning, skill library expansion, and self-improving code generation in Minecraft. | [ArXiv Link](https://arxiv.org/abs/2305.16291) |

---

## 💻 Top Open-Source Frameworks & SDKs

| Repository | Description | Link |
|------------|-------------|------|
| **LangGraph** | Industry-standard graph-based framework for stateful, multi-agent workflows with cycles and human-in-the-loop. | [GitHub Repo](https://github.com/langchain-ai/langgraph) |
| **Smolagents** | Minimalist, code-first agent framework from Hugging Face executing code actions natively. | [GitHub Repo](https://github.com/huggingface/smolagents) |
| **AutoGen** | Microsoft's multi-agent framework enabling complex conversational agent teams and task delegation. | [GitHub Repo](https://github.com/microsoft/autogen) |
| **CrewAI** | Role-playing, autonomous multi-agent framework for collaborative task execution. | [GitHub Repo](https://github.com/crewAIInc/crewAI) |
| **FastMCP** | High-level Python SDK for rapidly building Model Context Protocol (MCP) servers and tools. | [GitHub Repo](https://github.com/jlowin/fastmcp) |
| **Claude Code CLI** | Anthropic's agentic CLI tool for autonomous pair programming, tool invocation, and terminal execution. | [Anthropic Docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code) |

---

## 🎥 Must-Watch YouTube Videos & Free Lectures

| Video / Playlist | Creator | Description | Link |
|------------------|---------|-------------|------|
| **Functions, Tools, and Agents with LangChain** | DeepLearning.AI | Free course by Harrison Chase (LangChain Founder) on building tools, memory, and multi-agent systems. | [DeepLearning.AI Site](https://www.deeplearning.ai/short-courses/functions-tools-agents-langchain/) |
| **AI Agent Design Patterns** | Andrew Ng | Masterclass explaining reflection, tool use, planning, and multi-agent collaboration design patterns. | [YouTube Video](https://www.youtube.com/watch?v=sal78ACtGTc) |
| **Building Code-Executing Agents** | Hugging Face | Deep dive into Smolagents and code execution vs JSON tool calling for real-world reliability. | [Watch Video](https://www.youtube.com/watch?v=dSGS6-iGhyo) |

---

## 🎓 Free Courses & Open Curricula

| Course Title | Institution / Host | Focus | Link |
|--------------|-------------------|-------|------|
| **AI Agents in Practice** | DeepLearning.AI | Practical hands-on training on agent loops, memory, human-in-the-loop approval, and tool safety. | [DeepLearning.AI Course](https://www.deeplearning.ai/short-courses/) |
| **Agents Towards Production** | Community Hub | Open-source collection of production patterns, safety guardrails, and telemetry for agents. | [GitHub Repo](https://github.com/eugeneyan/awesome-ai-agents) |

---

## ⚙️ Code References & Hands-on Notebooks

- **[LangGraph Official Tutorials](https://github.com/langchain-ai/langgraph/tree/main/examples)** — Complete Python notebooks for human-in-the-loop approval, time travel state edits, and subgraphs.
- **[Model Context Protocol (MCP) Official SDKs & Examples](https://github.com/modelcontextprotocol/servers)** — Reference servers for filesystem, GitHub, Postgres, and Brave Search.
- **[Smolagents Tutorials](https://github.com/huggingface/smolagents/tree/main/examples)** — Minimal python code examples for web browsing agents, code agents, and multi-agent teams.
