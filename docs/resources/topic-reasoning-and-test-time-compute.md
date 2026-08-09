---
title: Topic Resources — Reasoning & Test-Time Compute
description: Curated research papers, YouTube videos, open-source repositories, and code references for Reasoning LLMs, Process Reward Models (PRMs), Chain-of-Thought (CoT), Search/MCTS, and Test-Time Compute Scaling.
---

# 🧠 Reasoning & Test-Time Compute — Topic Resources

Curated collection of landmark research papers, open-source repositories, YouTube videos, free masterclasses, and code references for **Reasoning Models, Chain-of-Thought (CoT), Process Reward Models (PRMs), Tree Search (MCTS), Self-Correction, and Test-Time Compute Scaling** (e.g., DeepSeek-R1, OpenAI o1/o3, Quiet-STaR).

---

## 📄 Landmark Papers & Essential Reading

| Paper / Reference | Authors / Year | Key Takeaways & Focus | Link |
|-------------------|----------------|-----------------------|------|
| **DeepSeek-R1: Incentivizing Reasoning Capability via RL** | DeepSeek AI (2025) | Demonstrates pure reinforcement learning (GRPO) without supervised warmups to elicit emerging chain-of-thought reasoning and self-reflection. | [ArXiv Link](https://arxiv.org/abs/2501.12948) |
| **Let's Verify Step by Step (Process Reward Models)** | Lightman et al. (OpenAI, 2023) | Introduces Process Reward Models (PRMs) trained to evaluate each intermediate reasoning step vs final outcome rewards (ORM). | [ArXiv Link](https://arxiv.org/abs/2305.20050) |
| **Tree of Thoughts: Deliberate Problem Solving with LLMs** | Yao et al. (2023) | Framework allowing search algorithms (BFS, DFS, MCTS) over arbitrary reasoning trees with intermediate evaluation steps. | [ArXiv Link](https://arxiv.org/abs/2305.04091) |
| **Quiet-STaR: Language Models Can Teach Themselves to Think** | Zelikman et al. (2024) | Enables LMs to generate rationale thoughts at every token position to improve future token predictions during pre-training. | [ArXiv Link](https://arxiv.org/abs/2403.09629) |
| **STaR: Bootstrapping Reasoning With Reasoning** | Zelikman et al. (2022) | Iterative loop generating reasoning rationales for correct answers and fine-tuning on self-generated solutions. | [ArXiv Link](https://arxiv.org/abs/2203.14465) |
| **SCoRe: Training Language Models to Self-Correct via Reinforcement Learning** | Kumar et al. (Google DeepMind, 2024) | Trains models to correct their own mistakes in a multi-turn RL setup without relying on external oracle feedback. | [ArXiv Link](https://arxiv.org/abs/2409.12917) |
| **Scaling LLM Test-Time Compute Optimally** | Snell et al. (Google DeepMind, 2024) | Demonstrates how trading off test-time compute (search & sampling) vs pre-training compute scales benchmark accuracy. | [ArXiv Link](https://arxiv.org/abs/2408.03314) |

---

## 💻 Top Open-Source Frameworks & Repositories

| Repository | Focus Area | Description | Link |
|------------|------------|-------------|------|
| **[Open-R1](https://github.com/huggingface/open-r1)** | Reasoning Fine-Tuning | Hugging Face's open implementation to reproduce DeepSeek-R1 via RL, synthetic data curation, and GRPO training. | [GitHub Repo](https://github.com/huggingface/open-r1) |
| **[veRL](https://github.com/volcengine/verl)** | Distributed RL for LLMs | Flexible, high-performance RL library from Volcengine optimized for training reasoning models with PPO and GRPO. | [GitHub Repo](https://github.com/volcengine/verl) |
| **[DeepSeek-R1](https://github.com/deepseek-ai/DeepSeek-R1)** | Open Weights & Distillations | Official repo releasing DeepSeek-R1 open weights, distilled LLaMA and Qwen models (1.5B to 70B parameters). | [GitHub Repo](https://github.com/deepseek-ai/DeepSeek-R1) |
| **[TinyZero](https://github.com/Jiayi-Pan/TinyZero)** | Minimalist R1 Reproduction | Clean, reproducible 300-line implementation of DeepSeek-R1 style RL reasoning training on countdown tasks. | [GitHub Repo](https://github.com/Jiayi-Pan/TinyZero) |
| **[search-r1](https://github.com/hkust-nlp/search-r1)** | RAG + Reasoning RL | Integrates search engine retrieval into RL reasoning trace generation for fact-checked self-reflection. | [GitHub Repo](https://github.com/hkust-nlp/search-r1) |

---

## 🎥 Must-Watch YouTube Videos & Free Lectures

| Video / Playlist | Creator | Description | Link |
|------------------|---------|-------------|------|
| **DeepSeek-R1 & Reinforcement Learning Breakthrough** | Andrej Karpathy | Deep technical breakdown of how pure RL incentivizes CoT reasoning, reward modeling, and distilled reasoning models. | [Watch Video](https://www.youtube.com/watch?v=7xTGNNLPyMI) |
| **DeepSeek-R1 Paper Walkthrough & PyTorch Code** | Umar Jamil | Line-by-line derivation of Group Relative Policy Optimization (GRPO), rule-based rewards, and token reasoning traces. | [Watch Video](https://www.youtube.com/@UmarJamil) |
| **Process Reward Models & Tree of Thoughts Explanation** | Yannic Kilcher | Paper breakdown of PRMs (Let's Verify Step by Step) and BFS/DFS tree search algorithms over LLM tokens. | [Watch Video](https://www.youtube.com/watch?v=w65l4T2pndE) |
| **Reasoning & Test-Time Compute Scaling Masterclass** | DeepLearning.AI | Masterclass explaining test-time compute tradeoffs, search strategies, and reward model architecture. | [Watch Video](https://www.youtube.com/watch?v=sal78ACtGTc) |

---

## 🎓 Free Courses & Interactive Guides

| Resource Title | Institution / Host | Focus | Link |
|----------------|-------------------|-------|------|
| **Hugging Face Deep RL Course** | Hugging Face | Free community course covering Policy Gradients, PPO, DPO, and GRPO for fine-tuning LLMs. | [Hugging Face Course](https://huggingface.co/learn/deep-rl-course/unit0/introduction) |
| **Reasoning Models Handbook** | Community Hub | Curated collection of tutorials, notebooks, and prompt templates for building reasoning chains. | [GitHub Repo](https://github.com/huggingface/open-r1) |

---

## ⚙️ Code References & Hands-on Notebooks

- **[TinyZero Countdown Task Notebook](https://github.com/Jiayi-Pan/TinyZero/blob/main/train.py)** — Run a complete GRPO RL reasoning loop locally in PyTorch on toy math tasks.
- **[Open-R1 Synthetic Data Pipeline](https://github.com/huggingface/open-r1/tree/main/src/open_r1)** — Pipelines for generating math/code CoT rationales and filtering step-by-step solutions.
- **[Process Reward Model Verification Notebook](https://github.com/openai/prm800k)** — OpenAI's official PRM800K dataset and step verification scripts.
