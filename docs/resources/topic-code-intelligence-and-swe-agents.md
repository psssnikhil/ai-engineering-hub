---
title: Topic Resources — Code Intelligence & SWE Agents
description: Curated papers, open-source repositories, YouTube lectures, free courses, and code references for Coding Agents, IDE Assistants, and Software Engineering Benchmarks.
---

# 💻 Code Intelligence & SWE Agents — Topic Resources

Curated list of top landmark papers, open-source repositories, video series, free courses, and code references for **Autonomous Coding Agents, Software Engineering Benchmarks (SWE-bench), IDE Assistants, and Sandboxed Code Execution**.

---

## 📄 Landmark Papers & Essential Reading

| Paper / Reference | Key Takeaways & Focus | Link |
|-------------------|-----------------------|------|
| **SWE-bench: Can Language Models Resolve Real-World GitHub Issues?** *(Jimenez et al., 2024)* | Standardized benchmark evaluating autonomous coding agents on resolving real-world software issues across open-source python repos. | [ArXiv Link](https://arxiv.org/abs/2310.06770) |
| **Evaluating Large Language Models Trained on Code (HumanEval / Codex)** *(Chen et al., 2021)* | OpenAI paper introducing HumanEval benchmark and functional correctness metrics (pass@k) for code generation models. | [ArXiv Link](https://arxiv.org/abs/2107.03374) |
| **Voyager: An Open-Ended Embodied Agent** *(Wang et al., 2023)* | Lifelong learning agent continuously writing, executing, and expanding a skill library of executable code. | [ArXiv Link](https://arxiv.org/abs/2305.10601) |

---

## 💻 Top Open-Source Coding Agents & Toolkits

| Repository | Description | Link |
|------------|-------------|------|
| **Claude Code CLI** | Anthropic's agentic CLI tool for autonomous pair programming, terminal execution, and context engineering. | [Anthropic Docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code) |
| **OpenHands (OpenDevin)** | Autonomous AI software engineer capable of complex dev tasks, code editing, and execution inside Docker containers. | [GitHub Repo](https://github.com/All-Hands-AI/OpenHands) |
| **Aider** | Command-line AI pair programming tool that edits local git repositories with git diff tracking. | [GitHub Repo](https://github.com/paul-gauthier/aider) |
| **Smolagents (CodeAgent)** | Hugging Face's lightweight Python library for building agents that execute code actions natively. | [GitHub Repo](https://github.com/huggingface/smolagents) |
| **FastMCP** | Python SDK for building Model Context Protocol (MCP) servers connecting coding agents to terminal tools & DBs. | [GitHub Repo](https://github.com/jlowin/fastmcp) |

---

## 🎥 Must-Watch YouTube Series & Videos

| Video / Playlist | Creator | Description | Link |
|------------------|---------|-------------|------|
| **Building Autonomous Coding Agents** | Hugging Face | Deep dive into code-execution agent loops vs JSON tool calling. | [YouTube Video](https://www.youtube.com/watch?v=0hM4-S9vW4c) |
| **SWE-bench Benchmark & AI Software Engineers** | Cameron Wolfe | Breakdown of SWE-bench dataset, harness evaluation, and sandboxed Docker containers. | [YouTube Channel](https://www.youtube.com/@cameronwolfe) |

---

## ⚙️ Code References & Hands-on Notebooks

- **[SWE-bench Harness & Runner](https://github.com/princeton-nlp/SWE-bench)** — Official Python code for evaluating agents against real GitHub pull requests.
- **[Smolagents Code Execution Examples](https://github.com/huggingface/smolagents/tree/main/examples)** — Notebooks implementing sandboxed python execution for agent loops.
