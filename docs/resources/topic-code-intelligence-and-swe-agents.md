---
title: Topic Resources — Code Intelligence & Software Engineering Agents
description: Curated research papers, YouTube videos, open-source repositories, and code references for Code LLMs, SWE-bench, Autonomous Coding Agents, Model Context Protocol (MCP), and Repo-level context retrieval.
---

# 💻 Code Intelligence & Software Engineering Agents — Topic Resources

Curated collection of landmark research papers, open-source repositories, YouTube videos, free masterclasses, and code references for **Code Generation Models, SWE-bench Benchmarks, Autonomous Software Engineering Agents, Model Context Protocol (MCP), and Repository-Level Context Retrieval** (e.g. Claude Code, SWE-agent, OpenHands, Aider).

---

## 📄 Landmark Papers & Essential Reading

| Paper / Reference | Authors / Year | Key Takeaways & Focus | Link |
|-------------------|----------------|-----------------------|------|
| **SWE-bench: Can Language Models Resolve Real-World GitHub Issues?** | Jimenez et al. (Princeton, 2024) | Standardized benchmark testing LLMs on resolving full GitHub repository issues, running test suites, and creating pull requests. | [ArXiv Link](https://arxiv.org/abs/2310.06770) |
| **SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering** | Yang et al. (Princeton, 2024) | Custom agent-computer interface (ACI) designed specifically for code editing, directory navigation, and test execution. | [ArXiv Link](https://arxiv.org/abs/2405.15793) |
| **Agentless: Demystifying LLM-based Software Engineering Agents** | Xia et al. (2024) | Demonstrates a simple hierarchical location-and-repair workflow matching complex agent framework accuracy at lower cost. | [ArXiv Link](https://arxiv.org/abs/2407.01489) |
| **Code Llama: Open Foundation Models for Code** | Rozière et al. (Meta, 2023) | Fine-tuned code models supporting long context (100k tokens), infilling (FIM), and multi-language execution. | [ArXiv Link](https://arxiv.org/abs/2308.12950) |
| **RepoCoder: Repository-Level Code Completion Through Iterative Retrieval Generation** | Zhang et al. (2023) | Iterative retrieval-augmented code generation leveraging repository context, cross-file imports, and signatures. | [ArXiv Link](https://arxiv.org/abs/2303.12570) |

---

## 💻 Top Open-Source Frameworks & SDKs

| Repository | Focus Area | Description | Link |
|------------|------------|-------------|------|
| **[SWE-agent](https://github.com/swe-agent/swe-agent)** | Autonomous Software Agent | Open-source agent environment designed to take GitHub issues and fix codebases autonomously. | [GitHub Repo](https://github.com/swe-agent/swe-agent) |
| **[OpenHands (OpenDevin)](https://github.com/All-Hands-AI/OpenHands)** | Autonomous AI Software Engineer | Open platform for AI software developers capable of terminal execution, browser control, and code edits. | [GitHub Repo](https://github.com/All-Hands-AI/OpenHands) |
| **[Aider](https://github.com/Aider-AI/aider)** | Pair Programming CLI | Command-line pair programming tool that edits files in local git repos and commits clean changes. | [GitHub Repo](https://github.com/Aider-AI/aider) |
| **[FastMCP](https://github.com/jlowin/fastmcp)** | Model Context Protocol SDK | High-level Python SDK for rapidly building Model Context Protocol (MCP) servers for agent tools. | [GitHub Repo](https://github.com/jlowin/fastmcp) |
| **[Claude Code CLI](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code)** | Anthropic Agentic CLI | Agentic terminal tool for codebase exploration, refactoring, test execution, and git workflow automation. | [Anthropic Docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code) |

---

## 🎥 Must-Watch YouTube Videos & Free Lectures

| Video / Playlist | Creator | Description | Link |
|------------------|---------|-------------|------|
| **SWE-bench & SWE-agent Deep Dive** | Princeton NLP | Authors explain agent-computer interfaces (ACI), benchmark design, and failure modes of coding agents. | [Watch Video](https://www.youtube.com/watch?v=DrLdvbkgmeA) |
| **Building Code-Executing Agents with Smolagents & FastMCP** | Hugging Face / FastMCP | Deep dive into native Python code execution vs JSON tool calling and setting up MCP servers. | [Watch Video](https://www.youtube.com/watch?v=sal78ACtGTc) |
| **Aider & Codebase Context Engineering** | Paul Gauthier (Aider Creator) | Breakdown of repository map construction using tree-sitter, git diff management, and prompt routing. | [Watch Video](https://www.youtube.com/watch?v=JCrhyFajxYE) |

---

## ⚙️ Code References & Hands-on Notebooks

- **[SWE-agent Official Evaluation Harness](https://github.com/swe-agent/swe-agent)** — Run automated code fixes on SWE-bench Lite benchmark problems locally.
- **[Model Context Protocol Server Examples](https://github.com/modelcontextprotocol/servers)** — Official Anthropic reference implementations for PostgreSQL, GitHub, FileSystem, and Terminal tools.
- **[Aider Repo Map Generator](https://github.com/Aider-AI/aider/tree/main/aider/repo_map.py)** — Source code reference implementation for generating tree-sitter repository structure maps for LLMs.
