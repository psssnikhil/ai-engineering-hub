---
title: Topic Resources — LLMOps, Serving, Evals & Observability
description: Curated papers, open-source repositories, YouTube lectures, free courses, and code references for LLMOps, LLM serving engines, evaluation pipelines, and tracing tools.
---

# ⚡ LLMOps, Serving, Evals & Observability — Topic Resources

Curated list of top landmark papers, open-source repositories, video series, free courses, and code references for **LLM Serving Engines, PagedAttention, LLMOps Infrastructure, LLM-as-a-Judge Evals, Observability, and Safety Guardrails**.

---

## 📄 Landmark Papers & Essential Reading

| Paper / Reference | Key Takeaways & Focus | Link |
|-------------------|-----------------------|------|
| **vLLM: Efficient Memory Management for Large Language Model Serving with PagedAttention** *(Kwon et al., 2023)* | Introduced PagedAttention, eliminating KV cache fragmentation and achieving 2-4x higher throughput. | [ArXiv Link](https://arxiv.org/abs/2309.06180) |
| **SGLang: Fast and Expressive Language Model Execution** *(Zheng et al., 2024)* | Introduces RadixAttention for automatic KV cache reuse across multi-turn agent calls and structured prompts. | [ArXiv Link](https://arxiv.org/abs/2312.07104) |
| **Fast Inference from Transformers via Speculative Decoding** *(Leviathan et al., 2023)* | Uses a small draft model to generate candidate tokens verified in parallel by a larger target model. | [ArXiv Link](https://arxiv.org/abs/2211.17192) |
| **DeepSeek-V3 Technical Report (Multi-Head Latent Attention)** *(DeepSeek AI, 2024)* | Introduces MLA to compress KV cache into low-rank latent vectors, achieving near-MHA quality with 93% memory savings. | [ArXiv Link](https://arxiv.org/abs/2412.19437) |
| **Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena** *(Zheng et al., 2023)* | Proved GPT-4 level LLM judges align 80%+ with human preference for evaluating chat assistants. | [ArXiv Link](https://arxiv.org/abs/2306.05685) |
| **HELM: Holistic Evaluation of Language Models** *(Liang et al., 2022)* | Standardized benchmarking methodology assessing accuracy, bias, toxicity, robustness, and efficiency. | [ArXiv Link](https://arxiv.org/abs/2211.09110) |
| **G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment** *(Liu et al., 2023)* | Framework using CoT prompts and form-based scoring to measure generation quality. | [ArXiv Link](https://arxiv.org/abs/2303.16634) |
| **Constitutional AI: Harmlessness from AI Feedback** *(Bai et al., 2022)* | Showed RLAIF (RL from AI Feedback) for aligning models against harmful prompts using explicit self-critique rules. | [ArXiv Link](https://arxiv.org/abs/2212.08073) |

---

## 💻 Top Open-Source Frameworks & Serving Engines

| Repository | Description | Link |
|------------|-------------|------|
| **vLLM** | High-throughput, memory-efficient LLM inference engine featuring PagedAttention and continuous batching. | [GitHub Repo](https://github.com/vllm-project/vllm) |
| **LiteLLM** | Lightweight proxy gateway allowing 100+ LLM APIs to be invoked via OpenAI format with load balancing & fallback. | [GitHub Repo](https://github.com/BerriAI/litellm) |
| **Ollama** | Get up and running with Llama 3, Mistral, and local LLMs locally with a simple API and CLI. | [GitHub Repo](https://github.com/ollama/ollama) |
| **Ragas** | Framework for evaluating Retrieval Augmented Generation pipelines with metrics like faithfulness and context recall. | [GitHub Repo](https://github.com/explodinggradients/ragas) |
| **Phoenix (Arize)** | Open-source AI observability platform for tracing LLM applications, agent steps, and automated evals. | [GitHub Repo](https://github.com/Ariadne-AI/phoenix) |
| **Promptfoo** | Command-line tool and library for testing, evaluating, and red-teaming LLM prompts and guardrails. | [GitHub Repo](https://github.com/promptfoo/promptfoo) |
| **NeMo Guardrails** | NVIDIA's framework for adding programmable safety guardrails, topic control, and hallucination checks. | [GitHub Repo](https://github.com/NVIDIA/NeMo-Guardrails) |

---

## 🎥 Must-Watch YouTube Videos & Free Lectures

| Video / Playlist | Creator | Description | Link |
|------------------|---------|-------------|------|
| **vLLM: High-Throughput Serving & PagedAttention** | Woosuk Kwon (vLLM Lead) | Deep architectural explanation of virtual memory management for KV caches in GPU memory. | [Search on YouTube →](https://www.youtube.com/results?search_query=Woosuk+Kwon+%28vLLM+Lead%29+vLLM%3A+High-Throughput+Serving+%26+PagedAttention) |
| **LLM Evaluation & Observability Masterclass** | Arize AI / Phoenix | Step-by-step video guides on instrumenting OpenTelemetry tracing, LLM evaluation, and drift detection. | [Search on YouTube →](https://www.youtube.com/results?search_query=Arize+AI+%2F+Phoenix+LLM+Evaluation+%26+Observability+Masterclass) |
| **Building Guardrails & Red Teaming** | DeepLearning.AI | Practical short course on securing LLM apps against prompt injection, jailbreaks, and PII leakage. | [DeepLearning.AI Site](https://www.deeplearning.ai/short-courses/) |

---

## 🎓 Free Courses & Open Curricula

| Course Title | Institution / Host | Focus | Link |
|--------------|-------------------|-------|------|
| **LLMOps: Building Real-World AI Applications** | DeepLearning.AI | End-to-end operationalization of LLM apps: CI/CD for prompts, automated testing, and cloud deployment. | [DeepLearning.AI Course](https://www.deeplearning.ai/short-courses/) |
| **Full Stack LLM Bootcamp** | FSDL | Free lectures on LLM stack, serving, prompt engineering, cost optimization, and evals. | [FSDL Course Site](https://fullstackdeeplearning.com/) |

---

## ⚙️ Code References & Hands-on Notebooks

- **[vLLM Official Examples](https://github.com/vllm-project/vllm/tree/main/examples)** — Serving custom models, multi-GPU tensor parallelism, and speculative decoding.
- **[LiteLLM Proxy Quickstart & Benchmarks](https://github.com/BerriAI/litellm/tree/main/cookbook)** — Code for setting up rate limits, budget tracking, and custom routing policies.
- **[Ragas Evaluation Tutorials](https://github.com/explodinggradients/ragas/tree/main/docs)** — Python notebooks for scoring RAG pipelines on faithfulness and answer relevance.
