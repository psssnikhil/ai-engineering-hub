---
title: Complete AI Engineering Research Papers Catalog
description: Categorized index of landmark AI/ML research papers covering Transformers, Reasoning, Multimodal, Code Agents, RAG, LLMOps, Serving, Fine-Tuning, Quantization, and Safety.
---

# 📄 Complete AI Engineering Research Papers Catalog

An annotated, categorized reference catalog of essential research papers referenced across the **AI Engineering Hub** handbook — complete with publication info, key takeaways, and direct ArXiv links.

---

## 🧠 1. Foundations, Transformer Architecture & Scaling Laws

| Paper Title | Authors / Year | Key Contribution & Takeaway | ArXiv Link |
|-------------|----------------|-----------------------------|------------|
| **Attention Is All You Need** | Vaswani et al. (2017) | Introduced the Transformer architecture based entirely on self-attention mechanisms without RNNs or CNNs. | [ArXiv:1706.03762](https://arxiv.org/abs/1706.03762) |
| **BERT: Pre-training of Deep Bidirectional Transformers** | Devlin et al. (2018) | Introduced bidirectional masked language modeling, revolutionizing transfer learning in NLP. | [ArXiv:1810.04805](https://arxiv.org/abs/1810.04805) |
| **Exploring the Limits of Transfer Learning (T5)** | Raffel et al. (2019) | Unified all NLP tasks into a single text-to-text input-output framework. | [ArXiv:1910.10683](https://arxiv.org/abs/1910.10683) |
| **Language Models are Few-Shot Learners (GPT-3)** | Brown et al. (2020) | Demonstrated scaling laws and in-context zero-shot / few-shot learning capabilities. | [ArXiv:2005.14165](https://arxiv.org/abs/2005.14165) |
| **Scaling Laws for Neural Language Models** | Kaplan et al. (2020) | Established empirical power-law scaling between compute, dataset size, parameters, and loss. | [ArXiv:2001.08361](https://arxiv.org/abs/2001.08361) |
| **An Empirical Analysis of Compute-Optimal Training (Chinchilla)** | Hoffmann et al. (2022) | Showed LLMs should be trained on equal scaling of tokens and parameters (20 tokens per parameter). | [ArXiv:2203.15556](https://arxiv.org/abs/2203.15556) |
| **RoFormer: Enhanced Transformer with Rotary Position Embedding** | Su et al. (2021) | Introduced RoPE relative positional encodings used by LLaMA, Mistral, and modern open-weight LLMs. | [ArXiv:2104.09864](https://arxiv.org/abs/2104.09864) |
| **Fast and Memory-Efficient Exact Attention (FlashAttention)** | Dao et al. (2022) | IO-aware exact attention algorithm reducing memory complexity from $O(N^2)$ to $O(N)$ with GPU SRAM tiling. | [ArXiv:2205.14135](https://arxiv.org/abs/2205.14135) |
| **FlashAttention-3: Fast Attention with Asynchronous Execution** | Shah et al. (2024) | Exploits FP8 Tensor Cores and asynchronous GPU warp execution on Hopper architecture for 2-3x speedup. | [ArXiv:2407.08608](https://arxiv.org/abs/2407.08608) |
| **Mamba: Linear-Time Sequence Modeling with Selective State Spaces** | Gu et al. (2023) | Selective state space model (SSM) enabling linear time $O(N)$ sequence length scaling without attention. | [ArXiv:2312.00752](https://arxiv.org/abs/2312.00752) |
| **LLaMA: Open and Efficient Foundation Language Models** | Touvron et al. (2023) | Open-weight foundation models trained strictly on publicly available datasets using SwiGLU & RoPE. | [ArXiv:2302.13971](https://arxiv.org/abs/2302.13971) |
| **Mixtral of Experts** | Jiang et al. (2024) | Sparse Mixture of Experts (MoE) 8x7B model selecting 2 active experts per token for fast inference. | [ArXiv:2401.15884](https://arxiv.org/abs/2401.15884) |

---

## ⚡ 2. Reasoning Models & Test-Time Compute

| Paper Title | Authors / Year | Key Contribution & Takeaway | ArXiv Link |
|-------------|----------------|-----------------------------|------------|
| **DeepSeek-R1: Incentivizing Reasoning Capability via RL** | DeepSeek AI (2025) | Demonstrates pure reinforcement learning without supervised warmups for eliciting chain-of-thought reasoning. | [ArXiv:2501.12948](https://arxiv.org/abs/2501.12948) |
| **Let's Verify Step by Step (Process Reward Models)** | Lightman et al. (2023) | Introduces Process Reward Models (PRMs) trained to evaluate individual intermediate reasoning steps vs outcome reward models. | [ArXiv:2305.20050](https://arxiv.org/abs/2305.20050) |
| **Quiet-STaR: Language Models Can Teach Themselves to Think** | Zelikman et al. (2024) | Enables LMs to generate rationale thoughts at every token position to improve future token predictions. | [ArXiv:2403.09629](https://arxiv.org/abs/2403.09629) |
| **Tree of Thoughts: Deliberate Problem Solving with LLMs** | Yao et al. (2023) | Enables tree-structured search (BFS/DFS) over intermediate reasoning paths for complex math and planning tasks. | [ArXiv:2305.04091](https://arxiv.org/abs/2305.04091) |
| **SCoRe: Training Language Models to Self-Correct via RL** | Kumar et al. (2024) | Teaches LLMs to self-correct reasoning errors in a multi-turn RL setup without oracle intervention. | [ArXiv:2409.12917](https://arxiv.org/abs/2409.12917) |

---

## 👁️ 3. Multimodal AI & Vision-Language Models

| Paper Title | Authors / Year | Key Contribution & Takeaway | ArXiv Link |
|-------------|----------------|-----------------------------|------------|
| **Learning Transferable Visual Models From Natural Language (CLIP)** | Radford et al. (2021) | Joint image-text contrastive embedding pre-training powering modern visual AI systems. | [ArXiv:2103.00020](https://arxiv.org/abs/2103.00020) |
| **Visual Instruction Tuning (LLaVA)** | Liu et al. (2023) | Connects CLIP vision encoder to LLaMA via visual projection layers trained on synthetic instruction data. | [ArXiv:2304.08485](https://arxiv.org/abs/2304.08485) |
| **ColPali: Efficient Document Retrieval with Vision Language Models** | Fuyu / ColPali Team (2024) | Indexes PDF page images directly using multi-vector VLM representations, bypassing OCR pipelines. | [ArXiv:2407.01449](https://arxiv.org/abs/2407.01449) |
| **Robust Speech Recognition via Large-Scale Weak Supervision (Whisper)** | Radford et al. (2022) | Encoder-decoder Transformer for end-to-end speech recognition across 68 languages. | [ArXiv:2212.04356](https://arxiv.org/abs/2212.04356) |

---

## 💻 4. Code Intelligence & Software Engineering Agents

| Paper Title | Authors / Year | Key Contribution & Takeaway | ArXiv Link |
|-------------|----------------|-----------------------------|------------|
| **SWE-bench: Can Language Models Resolve Real-World GitHub Issues?** | Jimenez et al. (2024) | Benchmark testing LLMs on resolving real-world open-source software bugs and repository PRs. | [ArXiv:2310.06770](https://arxiv.org/abs/2310.06770) |
| **SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering** | Yang et al. (2024) | Custom agent-computer interface (ACI) tailored for code editing, terminal execution, and file search. | [ArXiv:2405.15793](https://arxiv.org/abs/2405.15793) |
| **Agentless: Demystifying LLM-based Software Engineering Agents** | Xia et al. (2024) | Demonstrates a simple hierarchical location-and-repair workflow matching complex agent framework accuracy. | [ArXiv:2407.01489](https://arxiv.org/abs/2407.01489) |
| **Code Llama: Open Foundation Models for Code** | Rozière et al. (Meta, 2023) | Code foundation models supporting infilling, long context (100k tokens), and multi-language synthesis. | [ArXiv:2308.12950](https://arxiv.org/abs/2308.12950) |

---

## 📚 5. Advanced RAG & Vector Search

| Paper Title | Authors / Year | Key Contribution & Takeaway | ArXiv Link |
|-------------|----------------|-----------------------------|------------|
| **Retrieval-Augmented Generation for Knowledge-Intensive NLP** | Lewis et al. (2020) | Original RAG paper combining pre-trained seq2seq generator models with dense vector retrieval. | [ArXiv:2005.11401](https://arxiv.org/abs/2005.11401) |
| **Dense Passage Retrieval for Open-Domain QA (DPR)** | Karpukhin et al. (2020) | Proved dual-encoder dense vector embeddings outperform classical BM25 sparse keyword search. | [ArXiv:2004.04906](https://arxiv.org/abs/2004.04906) |
| **ColBERT: Late Interaction over BERT** | Khattab et al. (2020) | Introduced token-level late interaction matrix matching for fast, accurate multi-vector retrieval. | [ArXiv:2004.12832](https://arxiv.org/abs/2004.12832) |
| **Precise Zero-Shot Dense Retrieval (HyDE)** | Gao et al. (2022) | Hypothetical Document Embeddings — generates synthetic candidate answers to retrieve true source documents. | [ArXiv:2212.10496](https://arxiv.org/abs/2212.10496) |
| **From Local to Global Retrieval-Augmented Generation (GraphRAG)** | Edge et al. (Microsoft, 2024) | Combines knowledge graph extraction with community summaries for global dataset summarization. | [ArXiv:2404.16130](https://arxiv.org/abs/2404.16130) |
| **RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval** | Sarthi et al. (2024) | Builds hierarchical document summary trees to enable multi-level granular document retrieval. | [ArXiv:2401.18059](https://arxiv.org/abs/2401.18059) |
| **Self-RAG: Learning to Retrieve, Generate, and Critique** | Asai et al. (2023) | Endows LLMs with adaptive self-reflection tokens to decide *when* to retrieve and *how* to evaluate context. | [ArXiv:2310.11511](https://arxiv.org/abs/2310.11511) |

---

## 🤖 6. AI Agents & Tool Execution

| Paper Title | Authors / Year | Key Contribution & Takeaway | ArXiv Link |
|-------------|----------------|-----------------------------|------------|
| **ReAct: Synergizing Reasoning and Acting in Language Models** | Yao et al. (2022) | Standardized the Thought-Action-Observation loop driving modern autonomous agents. | [ArXiv:2210.03629](https://arxiv.org/abs/2210.03629) |
| **Toolformer: Language Models Can Teach Themselves to Use Tools** | Schick et al. (2023) | Self-supervised model learning where and how to call external APIs (calculators, search, Q&A). | [ArXiv:2302.04761](https://arxiv.org/abs/2302.04761) |
| **Reflexion: Language Agents with Verbal Reinforcement** | Shinn et al. (2023) | Autonomous agents reflecting on execution feedback, storing verbal episodic memories to prevent repeat mistakes. | [ArXiv:2303.11366](https://arxiv.org/abs/2303.11366) |
| **Generative Agents: Interactive Simulacra of Human Behavior** | Park et al. (2023) | Multi-agent sandbox simulation detailing memory streams, reflection summaries, and dynamic plan updates. | [ArXiv:2304.03442](https://arxiv.org/abs/2304.03442) |
| **Voyager: An Open-Ended Embodied Agent with LLMs** | Wang et al. (2023) | Lifelong learning agent in Minecraft continuously writing, executing, and expanding a skill library of Python code. | [ArXiv:2305.10601](https://arxiv.org/abs/2305.10601) |

---

## 💾 7. Long Context & Memory Architecture

| Paper Title | Authors / Year | Key Contribution & Takeaway | ArXiv Link |
|-------------|----------------|-----------------------------|------------|
| **RingAttention with Blockwise Transformers** | Liu et al. (2023) | Distributes sequence attention computation across multiple GPUs, enabling million-token context windows. | [ArXiv:2310.01889](https://arxiv.org/abs/2310.01889) |
| **MemGPT: Towards LLMs as Operating Systems** | Packer et al. (2023) | Manages bounded LLM context windows using OS-like virtual memory tiers (main context vs archival memory). | [ArXiv:2310.08560](https://arxiv.org/abs/2310.08560) |
| **Leave No Context Behind: Infini-attention** | Manya et al. (Google, 2024) | Integrates a compressive memory module into vanilla self-attention for infinite context handling. | [ArXiv:2404.07143](https://arxiv.org/abs/2404.07143) |

---

## ⚡ 8. Serving Engines & Quantization

| Paper Title | Authors / Year | Key Contribution & Takeaway | ArXiv Link |
|-------------|----------------|-----------------------------|------------|
| **vLLM: Memory Management with PagedAttention** | Kwon et al. (2023) | Introduced PagedAttention, virtualizing GPU memory for KV caches to achieve 2-4x higher serving throughput. | [ArXiv:2309.06180](https://arxiv.org/abs/2309.06180) |
| **SGLang: Fast and Expressive Language Model Execution** | Zheng et al. (2024) | RadixAttention framework for automatic KV cache reuse across multi-turn agent loops and structured generation. | [ArXiv:2312.07104](https://arxiv.org/abs/2312.07104) |
| **AWQ: Activation-aware Weight Quantization for LLMs** | Lin et al. (2023) | Protects 1% salient weight channels based on activation magnitude to achieve lossless 4-bit quantization. | [ArXiv:2306.00978](https://arxiv.org/abs/2306.00978) |
| **GPTQ: Accurate Post-Training Quantization for Transformers** | Frantar et al. (2022) | One-shot weight quantization method reducing LLMs to 3/4 bits in sub-second per layer execution time. | [ArXiv:2210.17323](https://arxiv.org/abs/2210.17323) |
| **The Era of 1-bit LLMs: BitNet b1.58** | Ma et al. (2024) | 1.58-bit ternary weight LLM architecture ($\{-1, 0, 1\}$) matching full-precision performance with zero matrix multiplications. | [ArXiv:2402.17764](https://arxiv.org/abs/2402.17764) |

---

## 🎛 9. Fine-Tuning & Model Alignment

| Paper Title | Authors / Year | Key Contribution & Takeaway | ArXiv Link |
|-------------|----------------|-----------------------------|------------|
| **LoRA: Low-Rank Adaptation of Large Language Models** | Hu et al. (2021) | Parameter-efficient fine-tuning freezing model base weights and injecting rank decomposition matrices. | [ArXiv:2106.09685](https://arxiv.org/abs/2106.09685) |
| **QLoRA: Efficient Finetuning of Quantized LLMs** | Dettmers et al. (2023) | 4-bit NormalFloat quantization + Double Quantization + Paged Optimizers enabling 65B model tuning on 48GB GPU. | [ArXiv:2305.14314](https://arxiv.org/abs/2305.14314) |
| **Direct Preference Optimization (DPO)** | Rafailov et al. (2023) | Reformulated RLHF to optimize LLMs directly on pairwise human preferences without training a separate reward model. | [ArXiv:2305.18290](https://arxiv.org/abs/2305.18290) |
| **DeepSeekMath: Group Relative Policy Optimization (GRPO)** | Shao et al. (2024) | Computes relative advantage over output groups to eliminate critic models during RL reasoning training. | [ArXiv:2402.03300](https://arxiv.org/abs/2402.03300) |
| **SimPO: Simple Preference Optimization with Reference-Free Reward** | Meng et al. (2024) | Reference-free reward formulation using sequence average log probability with target margins. | [ArXiv:2405.14734](https://arxiv.org/abs/2405.14734) |

---

## 🛡 10. Evaluation & Safety

| Paper Title | Authors / Year | Key Contribution & Takeaway | ArXiv Link |
|-------------|----------------|-----------------------------|------------|
| **HELM: Holistic Evaluation of Language Models** | Liang et al. (2022) | Comprehensive benchmarking framework evaluating accuracy, bias, toxicity, robustness, and efficiency. | [ArXiv:2211.09110](https://arxiv.org/abs/2211.09110) |
| **Judging LLM-as-a-Judge with MT-Bench & Chatbot Arena** | Zheng et al. (2023) | Validated strong LLMs (GPT-4) as fast, reliable judges for evaluating chat quality and pairwise model responses. | [ArXiv:2306.05685](https://arxiv.org/abs/2306.05685) |
| **Constitutional AI: Harmlessness from AI Feedback** | Bai et al. (2022) | Replaced human critique with self-critique guided by explicit principles (Constitutional RLAIF). | [ArXiv:2212.08073](https://arxiv.org/abs/2212.08073) |
