---
title: Topic Resources — LLM Reasoning & Test-Time Compute
description: Curated papers, open-source repositories, YouTube lectures, free courses, and code references for LLM Reasoning Models, Process Reward Models (PRMs), and Test-Time Compute Scaling.
---

# 🧩 LLM Reasoning & Test-Time Compute — Topic Resources

Curated list of top landmark papers, open-source repositories, video series, free courses, and code references for **Reasoning LLMs (DeepSeek-R1, o1/o3 paradigm), Process Reward Models (PRMs), Search over Chain-of-Thought (MCTS, ToT), and Test-Time Compute Scaling**.

---

## 📄 Landmark Papers & Essential Reading

| Paper / Reference | Key Takeaways & Focus | Link |
|-------------------|-----------------------|------|
| **DeepSeek-R1: Incentivizing Reasoning Capability via RL** *(DeepSeek AI, 2025)* | Landmark paper proving pure RL without supervised warmups elicits chain-of-thought reasoning, self-verification, and long reflection. | [ArXiv Link](https://arxiv.org/abs/2501.12948) |
| **Let's Verify Step by Step (Process Reward Models)** *(Lightman et al., 2023)* | Proves Process Reward Models (PRMs) trained on step-by-step correctness outperform Outcome Reward Models (ORMs) for math & logic. | [ArXiv Link](https://arxiv.org/abs/2305.20050) |
| **Tree of Thoughts: Deliberate Problem Solving with LLMs** *(Yao et al., 2023)* | Tree search (BFS/DFS) over intermediate CoT steps, enabling lookahead planning and self-backtracking. | [ArXiv Link](https://arxiv.org/abs/2305.04091) |
| **Quiet-STaR: Language Models Can Teach Themselves to Think** *(Zelikman et al., 2024)* | Enables language models to generate rationale thoughts at arbitrary token positions before predicting text. | [ArXiv Link](https://arxiv.org/abs/2403.09629) |
| **Scaling LLM Test-Time Compute Optimally** *(Snell et al., 2024)* | Analyzes trade-offs between pre-training compute vs search compute at inference time. | [ArXiv Link](https://arxiv.org/abs/2408.03314) |

---

## 💻 Top Open-Source Repositories & Search Engines

| Repository | Description | Link |
|------------|-------------|------|
| **DeepSeek-R1** | Official repository for DeepSeek-R1 reasoning models, distillation weights, and inference benchmarks. | [GitHub Repo](https://github.com/deepseek-ai/DeepSeek-R1) |
| **Open-R1** | Hugging Face's open-source effort to fully reproduce DeepSeek-R1 training pipeline with TRL & vLLM. | [GitHub Repo](https://github.com/huggingface/open-r1) |
| **Searchformer** | Facebook Research's framework for training transformers to plan and execute search algorithms (A*, MCTS). | [GitHub Repo](https://github.com/facebookresearch/searchformer) |
| **vLLM (Reasoning Mode)** | High-throughput serving engine supporting long CoT output generation and speculative decoding. | [GitHub Repo](https://github.com/vllm-project/vllm) |

---

## 🎥 Must-Watch YouTube Series & Videos

| Video / Playlist | Creator | Description | Link |
|------------------|---------|-------------|------|
| **DeepSeek-R1 & RL Reasoning Breakdown** | Umar Jamil | Line-by-line mathematical breakdown of DeepSeek-R1 GRPO (Group Relative Policy Optimization) and reward modeling. | [YouTube Video](https://www.youtube.com/@UmarJamil) |
| **OpenAI o1 & Test-Time Scaling** | Cameron Wolfe | Deep dive into inference-time compute scaling, search trees, and process supervision. | [YouTube Channel](https://www.youtube.com/@cameronwolfe) |
| **Process Reward Models (PRMs) Explained** | Yannic Kilcher | Paper breakdown of OpenAI's *Let's Verify Step by Step* and step-level supervision. | [YouTube Video](https://www.youtube.com/watch?v=0hM4-S9vW4c) |

---

## ⚙️ Code References & Hands-on Notebooks

- **[Hugging Face Open-R1 Recipes](https://github.com/huggingface/open-r1/tree/main/src/open_r1)** — Python scripts for GRPO training, evaluation, and distillation.
- **[Tree of Thoughts PyTorch Reference](https://github.com/princeton-nlp/tree-of-thought-llm)** — Official code for ToT search algorithms over LLM prompts.
