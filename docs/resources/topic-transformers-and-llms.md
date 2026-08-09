---
title: Topic Resources — Transformers & LLM Fundamentals
description: Curated papers, open-source repositories, YouTube lectures, free courses, and code references for Transformers and LLM architecture.
---

# 🧠 Transformers & LLM Architecture — Topic Resources

Curated list of top landmark papers, open-source repositories, video series, free courses, and code references for mastering **Neural Networks, Transformers, Attention Mechanisms, and Large Language Model Architectures**.

---

## 📄 Landmark Papers & Essential Reading

| Paper / Reference | Key Takeaways & Focus | Link |
|-------------------|-----------------------|------|
| **Attention Is All You Need** *(Vaswani et al., 2017)* | Introduced the Transformer architecture relying entirely on self-attention mechanisms without RNNs/CNNs. | [ArXiv Link](https://arxiv.org/abs/1706.03762) |
| **BERT: Pre-training of Deep Bidirectional Transformers** *(Devlin et al., 2018)* | Showed bidirectional masked language modeling for downstream NLP transfer learning. | [ArXiv Link](https://arxiv.org/abs/1810.04805) |
| **Language Models are Few-Shot Learners (GPT-3)** *(Brown et al., 2020)* | Demonstrated scaling laws, zero-shot, and few-shot in-context learning capabilities. | [ArXiv Link](https://arxiv.org/abs/2005.14165) |
| **RoFormer: Enhanced Transformer with Rotary Position Embedding** *(Su et al., 2021)* | Introduced RoPE, the dominant positional encoding used in LLaMA, Mistral, and Claude. | [ArXiv Link](https://arxiv.org/abs/2104.09864) |
| **GQA: Training Generalized Multi-Query Transformer Models** *(Ainslie et al., 2023)* | Grouped-Query Attention reducing KV cache memory bandwidth bottlenecks during LLM inference. | [ArXiv Link](https://arxiv.org/abs/2305.13245) |
| **Mamba: Linear-Time Sequence Modeling with Selective State Spaces** *(Gu et al., 2023)* | Introduced selective SSM architecture achieving $O(N)$ linear sequence length scaling without attention. | [ArXiv Link](https://arxiv.org/abs/2312.00752) |
| **FlashAttention: Fast and Memory-Efficient Exact Attention** *(Dao et al., 2022)* | IO-aware exact attention algorithm reducing memory complexity from $O(N^2)$ to $O(N)$ speedups. | [ArXiv Link](https://arxiv.org/abs/2205.14135) |
| **FlashAttention-3: Fast Attention with Asynchronous Execution** *(Shah et al., 2024)* | Exploits FP8 Tensor Cores and asynchronous GPU warp execution on Hopper architecture for 2-3x speedup. | [ArXiv Link](https://arxiv.org/abs/2407.08608) |

---

## 💻 Top Open-Source Repositories & Implementations

| Repository | Description | Link |
|------------|-------------|------|
| **nanoGPT** | Andrej Karpathy's cleanest, fastest repository for training/finetuning medium-sized GPTs in PyTorch. | [GitHub Repo](https://github.com/karpathy/nanoGPT) |
| **micrograd** | Tiny autograd engine implementing backpropagation over a dynamically built DAG with PyTorch-like API. | [GitHub Repo](https://github.com/karpathy/micrograd) |
| **transformers (Hugging Face)** | State-of-the-art Machine Learning for PyTorch, TensorFlow, and JAX with pretrained weights. | [GitHub Repo](https://github.com/huggingface/transformers) |
| **Triton** | Python-based programming language and compiler for writing custom GPU kernels (FlashAttention, KV cache). | [GitHub Repo](https://github.com/triton-lang/triton) |
| **tiktoken** | Fast BPE tokeniser for use with OpenAI's models in Rust and Python. | [GitHub Repo](https://github.com/openai/tiktoken) |

---

## 🎥 Must-Watch YouTube Series & Videos

| Video / Playlist | Creator | Description | Link |
|------------------|---------|-------------|------|
| **Neural Networks: Zero to Hero** | Andrej Karpathy | 7-part video series building micrograd, makemore, WaveNet, GPT-2 from scratch in PyTorch. | [YouTube Playlist](https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUbF9GE) |
| **Deep Learning Series** | 3Blue1Brown | Unrivaled visual intuition for gradient descent, backpropagation, and self-attention. | [YouTube Playlist](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi) |
| **Coding Transformer / Attention Papers** | Umar Jamil | Line-by-line PyTorch implementation of Attention Is All You Need and LLaMA architecture. | [Search on YouTube →](https://www.youtube.com/results?search_query=Umar+Jamil+Coding+Transformer+%2F+Attention+Papers) |
| **LLM Visualization & Intuition** | Jay Alammar | Visual blog posts & videos explaining Transformer matrices, embeddings, and attention. | [Blog / Site](https://jalammar.github.io/illustrated-transformer/) |

---

## 🎓 Free Courses & Open Curricula

| Course Title | Institution / Host | Focus | Link |
|--------------|-------------------|-------|------|
| **CS224N: Natural Language Processing with Deep Learning** | Stanford University | Word vectors, sequence models, Transformers, pre-training, and scaling laws. | [Stanford Course Site](https://web.stanford.edu/class/cs224n/) |
| **CS336: Language Modeling from Scratch** | Stanford University | Deep technical lectures on data curation, distributed training, hardware utilization, & inference. | [Stanford CS336 Site](https://stanford-cs336.github.io/spring2024/) |
| **Hugging Face NLP Course** | Hugging Face | Free practical course on Transformers, Tokenization, Fine-Tuning, and Datasets. | [Hugging Face Course](https://huggingface.co/learn/nlp-course/chapter1/1) |

---

## ⚙️ Code References & Hands-on Notebooks

- **[Build a Large Language Model From Scratch (Repo)](https://github.com/rasbt/LLMs-from-scratch)** — Sebastian Raschka's step-by-step code matching his Manning book.
- **[Illustrated Transformer Notebooks](https://github.com/jalammar/illustrated-transformer)** — PyTorch execution matching visual transformer walkthroughs.
- **[OpenAI Cookbook — Embeddings & Tokenization](https://cookbook.openai.com/)** — Practical token counting, embedding generation, and vector similarity calculations.
