---
title: Topic Resources — Fine-Tuning & Model Alignment
description: Curated papers, open-source repositories, YouTube lectures, free courses, and code references for Fine-Tuning (PEFT, LoRA, QLoRA) and Alignment (DPO, RLHF).
---

# 🎛 Fine-Tuning & Model Alignment — Topic Resources

Curated list of top landmark papers, open-source repositories, video series, free courses, and code references for **Supervised Fine-Tuning (SFT), Parameter-Efficient Fine-Tuning (PEFT / LoRA / QLoRA), Direct Preference Optimization (DPO), and Reinforcement Learning with Human Feedback (RLHF)**.

---

## 📄 Landmark Papers & Essential Reading

| Paper / Reference | Key Takeaways & Focus | Link |
|-------------------|-----------------------|------|
| **LoRA: Low-Rank Adaptation of Large Language Models** *(Hu et al., 2021)* | Freezes pre-trained weights and injects trainable rank decomposition matrices, reducing trainable parameters by 10,000x. | [ArXiv Link](https://arxiv.org/abs/2106.09685) |
| **QLoRA: Efficient Finetuning of Quantized LLMs** *(Dettmers et al., 2023)* | 4-bit NormalFloat (NF4) quantization + Double Quantization + Paged Optimizers enabling 65B LLM fine-tuning on a single 48GB GPU. | [ArXiv Link](https://arxiv.org/abs/2305.14314) |
| **Direct Preference Optimization: Your Language Model is Secretly a Reward Model** *(Rafailov et al., 2023)* | Solves RLHF optimization via simple classification loss without needing a separate reward model or PPO training loop. | [ArXiv Link](https://arxiv.org/abs/2305.18290) |
| **DeepSeekMath: Pushing the Limits of Mathematical Reasoning (GRPO)** *(Shao et al., 2024)* | Introduces Group Relative Policy Optimization, computing advantage relative to a group of sampled outputs to eliminate critic models. | [ArXiv Link](https://arxiv.org/abs/2402.03300) |
| **SimPO: Simple Preference Optimization with Reference-Free Reward** *(Meng et al., 2024)* | Uses average log probability as implicit reward with a target margin, outperforming DPO without reference models. | [ArXiv Link](https://arxiv.org/abs/2405.14734) |
| **Orpo: Monolithic Preference Optimization Without Reference Model** *(Hong et al., 2024)* | Combines SFT and alignment into a single loss function without requiring a reference model during training. | [ArXiv Link](https://arxiv.org/abs/2403.07691) |

---

## 💻 Top Open-Source Frameworks & Toolkits

| Repository | Description | Link |
|------------|-------------|------|
| **Unsloth** | 2-5x faster LLM fine-tuning with 80% less memory usage for LLaMA, Gemma, and Mistral models. | [GitHub Repo](https://github.com/unslothai/unsloth) |
| **Axolotl** | Easy-to-use framework for post-training LLMs supporting LoRA, QLoRA, DPO, and multi-node distributed training. | [GitHub Repo](https://github.com/axolotl-ai-cloud/axolotl) |
| **LLaMA-Factory** | Unified efficient fine-tuning framework supporting 100+ LLMs with easy web GUI and CLI options. | [GitHub Repo](https://github.com/hiyouga/LLaMA-Factory) |
| **TRL (Transformer Reinforcement Learning)** | Hugging Face's library for post-training LLMs using SFT, PPO, DPO, ORPO, and reward modeling. | [GitHub Repo](https://github.com/huggingface/trl) |
| **PEFT (Hugging Face)** | State-of-the-art parameter-efficient fine-tuning methods integrated into Hugging Face Transformers. | [GitHub Repo](https://github.com/huggingface/peft) |

---

## 🎥 Must-Watch YouTube Videos & Free Lectures

| Video / Playlist | Creator | Description | Link |
|------------------|---------|-------------|------|
| **LoRA & QLoRA Mathematical Breakdown** | Umar Jamil | Line-by-line breakdown and PyTorch matrix implementation of Low-Rank Adaptation and 4-bit NF4 quantization. | [YouTube Video](https://www.youtube.com/watch?net=123) |
| **Fine-Tuning LLMs with Unsloth & TRL** | Sebastian Raschka | Step-by-step practical guide on fine-tuning open-weight models on custom dataset formatting. | [Search on YouTube →](https://www.youtube.com/results?search_query=Sebastian+Raschka+Fine-Tuning+LLMs+with+Unsloth+%26+TRL) |
| **DPO vs PPO Alignment** | Cameron Wolfe | Deep dive video explaining mathematical foundations of Direct Preference Optimization vs PPO. | [Search on YouTube →](https://www.youtube.com/results?search_query=Cameron+Wolfe+DPO+vs+PPO+Alignment) |

---

## 🎓 Free Courses & Open Curricula

| Course Title | Institution / Host | Focus | Link |
|--------------|-------------------|-------|------|
| **Finetuning Large Language Models** | DeepLearning.AI | Free short course by Sharon Zhou (Lamini CEO) on dataset prep, instruction tuning, and model evaluation. | [DeepLearning.AI Course](https://www.deeplearning.ai/short-courses/finetuning-large-language-models/) |
| **Open LLM Leaderboard & Alignment Guide** | Hugging Face | Guidelines and benchmark datasets for instruction tuning and preference alignment. | [Hugging Face Docs](https://huggingface.co/docs/trl/index) |

---

## ⚙️ Code References & Hands-on Notebooks

- **[Unsloth Colab Notebooks](https://github.com/unslothai/unsloth#notebooks)** — Free 1-click Google Colab notebooks for fine-tuning LLaMA 3, Mistral, and Gemma models.
- **[TRL DPO & SFT Examples](https://github.com/huggingface/trl/tree/main/examples)** — Complete Python scripts for training preference models and running DPO fine-tuning.
- **[Raschka's LLM Fine-Tuning Code](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch07)** — Pure PyTorch implementation of instruction fine-tuning and DPO.
