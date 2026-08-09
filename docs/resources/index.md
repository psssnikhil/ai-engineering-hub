---
title: Ultimate AI Engineering Resources
description: Curated list of top GitHub repositories, videos, blogs, books, and frameworks for AI Engineers
---

# AI Engineering Resources

A curated collection of the most valuable open-source repositories, video series, technical blogs, papers, free courses, and code references for mastering AI engineering — from foundational deep learning to production agents and LLM serving.

---

## 🎯 Resources by Major Topic

Jump directly to a dedicated resource guide combining **landmark papers, top GitHub repositories, YouTube series, free courses, and code references** for each major AI topic:

| Major Topic | What's Included | Link |
|-------------|-----------------|------|
| **🧠 Transformers & LLM Architecture** | Vaswani, BERT, GPT-3, RoPE, FlashAttention, nanoGPT, Karpathy series, Stanford CS224N/CS336 | [Transformers & LLM Resources](topic-transformers-and-llms.md) |
| **🧩 Reasoning & Test-Time Compute** | DeepSeek-R1, PRMs, Tree of Thoughts, MCTS, Quiet-STaR, Open-R1, GRPO | [Reasoning & Test-Time Compute](topic-reasoning-and-test-time-compute.md) |
| **👁 Multimodal AI & VLMs** | CLIP, LLaVA, Flamingo, Qwen-VL, Multimodal RAG, Whisper, Voice Agents | [Multimodal AI & VLM Resources](topic-multimodal-and-vlm.md) |
| **💻 Code Intelligence & SWE Agents** | SWE-bench, HumanEval, Claude Code CLI, OpenHands, Aider, Smolagents | [Code Intelligence & SWE Agents](topic-code-intelligence-and-swe-agents.md) |
| **📚 RAG & Vector Search** | RAG, DPR, ColBERT, HyDE, LlamaIndex, Qdrant, Chroma, DeepLearning.AI RAG, Vector DB Academy | [RAG & Vector Search Resources](topic-rag-and-vector-search.md) |
| **🤖 AI Agents & Harness Engineering** | ReAct, Toolformer, Generative Agents, LangGraph, Smolagents, AutoGen, FastMCP, Claude Code | [AI Agents & Harness Resources](topic-agents-and-harnesses.md) |
| **⚡ LLMOps, Serving, Evals & Safety** | vLLM, PagedAttention, LiteLLM, Ragas, Phoenix, MT-Bench, HELM, Guardrails, Red Teaming | [LLMOps & Serving Resources](topic-llmops-evals-serving.md) |
| **🎛 Fine-Tuning & Model Alignment** | LoRA, QLoRA, SFT, DPO, RLHF, Unsloth, Axolotl, LLaMA-Factory, TRL, Raschka guides | [Fine-Tuning & Alignment Resources](topic-finetuning-and-alignment.md) |

---

## ⭐️ Top GitHub Repositories

| Repository | Focus Area | Description |
|------------|------------|-------------|
| **[vLLM](https://github.com/vllm-project/vllm)** | LLM Serving | High-throughput, memory-efficient LLM inference engine with PagedAttention. |
| **[LiteLLM](https://github.com/BerriAI/litellm)** | API Gateway | Call 100+ LLM APIs using a standardized OpenAI format with cost tracking and fallbacks. |
| **[LangGraph](https://github.com/langchain-ai/langgraph)** | Agent Framework | Build stateful, multi-agent workflows with cyclic graphs and human-in-the-loop controls. |
| **[Smolagents](https://github.com/huggingface/smolagents)** | Code Agents | Lightweight library from Hugging Face for building agents that execute Python code actions. |
| **[LlamaIndex](https://github.com/run-llama/llama_index)** | RAG & Data | Data framework to connect private data sources (PDFs, DBs, APIs) to LLMs. |
| **[AutoGen](https://github.com/microsoft/autogen)** | Multi-Agent | Framework by Microsoft enabling multi-agent conversation and task orchestration. |
| **[DSPy](https://github.com/stanfordnlp/dspy)** | Prompt Optimization | Programmatically optimize LM prompts and module weights instead of manual prompting. |
| **[Instructor](https://github.com/jxnl/instructor)** | Structured Outputs | Extract structured data (JSON matching Pydantic schemas) reliably from LLMs. |
| **[Ragas](https://github.com/explodinggradients/ragas)** | RAG Evals | Framework for evaluating Retrieval Augmented Generation pipelines with metrics. |
| **[Triton](https://github.com/triton-lang/triton)** | GPU Kernel Programming | Open-source Python-like programming language and compiler for writing custom GPU kernels. |

---

## 🎬 Must-Watch Videos & Courses

- **[Andrej Karpathy — Neural Networks: Zero to Hero](https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUbF9GE)**  
  The ultimate code-first series building Micrograd, Makemore, and GPT-2 from scratch using PyTorch.
- **[3Blue1Brown — Deep Learning Series](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi)**  
  Unrivaled visual intuition for gradient descent, backpropagation, attention mechanisms, and linear algebra.
- **[Stanford CS224N — NLP with Deep Learning](https://web.stanford.edu/class/cs224n/)**  
  Stanford’s flagship course covering word embeddings, sequence-to-sequence models, transformers, and pre-training.
- **[Stanford CS336 — Language Modeling from Scratch](https://stanford-cs336.github.io/spring2024/)**  
  Deep technical lectures on data curation, distributed training, hardware utilization, and LLM inference algorithms.
- **[Umar Jamil — Paper Walkthroughs](https://www.youtube.com/@UmarJamil)**  
  Line-by-line PyTorch code walkthroughs of landmark papers (Attention is All You Need, LLaMA, LoRA, FlashAttention).

---

## 📰 Blogs & Newsletters

- **[Chip Huyen's Blog](https://huyenchip.com/blog/)**  
  In-depth articles on ML systems design, real-time machine learning, and moving AI from prototype to production.
- **[Eugene Yan's Blog](https://eugeneyan.com/)**  
  Practical guides on LLM patterns, search/recommendation systems, evals, and real-world AI engineering tradeoffs.
- **[Lilian Weng (Lil'Log)](https://lilianweng.github.io/posts/)**  
  Comprehensive technical synthesis of research frontiers including autonomous agents, RLHF, and prompt engineering.
- **[Anthropic Research & Engineering](https://www.anthropic.com/news)**  
  Insights into constitutional AI, interpretability, prompt design, and system architecture behind Claude.
- **[OpenAI Cookbook](https://cookbook.openai.com/)**  
  Hands-on recipes, code snippets, and integration guides for common LLM application patterns.
- **[Ahead of AI (Sebastian Raschka)](https://magazine.sebastianraschka.com/)**  
  Clear, breakdown articles explaining recent AI papers, fine-tuning techniques, and model architectures.

---

## 📚 Essential Books

- **[Designing Machine Learning Systems](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/)** *(Chip Huyen)*  
  The standard textbook for data engineering, model monitoring, deployment pipelines, and system trade-offs.
- **[Build a Large Language Model From Scratch](https://www.manning.com/books/build-a-large-language-model-from-scratch)** *(Sebastian Raschka)*  
  Step-by-step tutorial implementing every component of a Transformer LLM from tokenization to instruction tuning.
- **[Deep Learning](https://www.deeplearningbook.org/)** *(Ian Goodfellow, Yoshua Bengio, Aaron Courville)*  
  The foundational reference for mathematical theory, optimization, and neural network fundamentals.
- **[Hands-On Machine Learning](https://www.oreilly.com/library/view/hands-on-machine-learning/9781098125608/)** *(Aurélien Géron)*  
  Practical introduction to standard ML workflows, Scikit-Learn, PyTorch, and model evaluation.

---

## 🔗 Handbook Reference Indexes

- **[Transformers & LLM Architecture Resources](topic-transformers-and-llms.md)** — Dedicated topic guide
- **[Reasoning & Test-Time Compute Resources](topic-reasoning-and-test-time-compute.md)** — Dedicated topic guide
- **[Multimodal AI & VLM Resources](topic-multimodal-and-vlm.md)** — Dedicated topic guide
- **[Code Intelligence & SWE Agent Resources](topic-code-intelligence-and-swe-agents.md)** — Dedicated topic guide
- **[RAG & Vector Search Resources](topic-rag-and-vector-search.md)** — Dedicated topic guide
- **[AI Agents & Harness Resources](topic-agents-and-harnesses.md)** — Dedicated topic guide
- **[LLMOps & Serving Resources](topic-llmops-evals-serving.md)** — Dedicated topic guide
- **[Fine-Tuning & Alignment Resources](topic-finetuning-and-alignment.md)** — Dedicated topic guide
- **[Technical Blogs & Architecture Guides](blogs-and-guides.md)** — Curated engineering blogs (Aman Chadha, Lil'Log, Eugene Yan, Chip Huyen, Raschka)
- **[Essential Papers](essential-papers.md)** — landmark research papers referenced across lessons
- **[Essential Videos](essential-videos.md)** — core lectures and video walkthroughs
- **[Open Source Hubs](open-source-hubs.md)** — curated hubs (Agents Towards Production, RAG Techniques)
- **[Courses & Communities](courses-and-communities.md)** — free interactive courses and engineering forums
- **[Complete Papers Catalog](papers.md)** — complete annotated research paper catalog
- **[Complete Videos Catalog](videos.md)** — complete video series and lecture catalog
- **[Tools & Frameworks Index](tools-and-libraries.md)** — complete SDK, vector DB, and framework index
