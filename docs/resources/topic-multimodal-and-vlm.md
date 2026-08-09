---
title: Topic Resources — Multimodal AI & Vision-Language Models (VLMs)
description: Curated papers, open-source repositories, YouTube lectures, free courses, and code references for Vision-Language Models (VLMs), Multimodal RAG, and Voice Agents.
---

# 👁 Multimodal AI & Vision-Language Models — Topic Resources

Curated list of top landmark papers, open-source repositories, video series, free courses, and code references for **Vision-Language Models (VLMs), Multimodal RAG, Image Tool Calling, and Speech/Voice Agents**.

---

## 📄 Landmark Papers & Essential Reading

| Paper / Reference | Key Takeaways & Focus | Link |
|-------------------|-----------------------|------|
| **Learning Transferable Visual Models from Natural Language (CLIP)** *(Radford et al., 2021)* | Foundational dual-encoder architecture aligning image and text representations in a shared embedding space. | [ArXiv Link](https://arxiv.org/abs/2103.00020) |
| **Visual Instruction Tuning (LLaVA)** *(Liu et al., 2023)* | Connects a vision encoder (CLIP) to a projection matrix and LLM base for general-purpose visual instruction following. | [ArXiv Link](https://arxiv.org/abs/2304.08485) |
| **Flamingo: a Visual Language Model for Few-Shot Learning** *(Alayrac et al., 2022)* | Interleaved cross-attention layers fusing visual features with autoregressive LLM decoding. | [ArXiv Link](https://arxiv.org/abs/2204.14198) |
| **Qwen-VL: A Versatile Vision-Language Model** *(Bai et al., 2023)* | High-resolution vision-language model supporting grounding, bounding box detection, and multi-image processing. | [ArXiv Link](https://arxiv.org/abs/2308.12966) |

---

## 💻 Top Open-Source Repositories & SDKs

| Repository | Description | Link |
|------------|-------------|------|
| **LLaVA** | Official open-source implementation for training and fine-tuning LLaVA vision-language models. | [GitHub Repo](https://github.com/haotian-liu/LLaVA) |
| **transformers (VLM Pipeline)** | Hugging Face support for Qwen-VL, IDEFICS, LLaVA-NeXT, and Paligemma models. | [Hugging Face Docs](https://huggingface.co/docs/transformers/main/en/model_doc/llava) |
| **Whisper** | OpenAI's robust speech recognition model trained on 680,000 hours of multilingual audio. | [GitHub Repo](https://github.com/openai/whisper) |
| **vLLM (Multimodal Inference)** | Serving VLM models (LLaVA, Qwen-VL) with high-throughput PagedAttention. | [vLLM Docs](https://docs.vllm.ai) |

---

## 🎥 Must-Watch YouTube Series & Videos

| Video / Playlist | Creator | Description | Link |
|------------------|---------|-------------|------|
| **Vision Transformers (ViT) & CLIP Architecture** | Umar Jamil | Line-by-line PyTorch implementation of Vision Transformers (ViT) and CLIP contrastive loss. | [YouTube Video](https://www.youtube.com/@UmarJamil) |
| **Multimodal RAG with LlamaIndex** | Jerry Liu | Step-by-step video tutorial on indexing images, tables, and PDFs for multimodal retrieval. | [YouTube Video](https://www.youtube.com/watch?v=0hM4-S9vW4c) |

---

## ⚙️ Code References & Hands-on Notebooks

- **[LlamaIndex Multimodal RAG Recipes](https://github.com/run-llama/llama_index/tree/main/docs/docs/examples/multi_modal)** — Notebooks for multi-modal vector search, chart extraction, and GPT-4V indexing.
- **[Hugging Face LLaVA Fine-Tuning Guide](https://huggingface.co/blog/fine-tune-readme)** — Code tutorial for fine-tuning vision-language models on custom image-text data.
