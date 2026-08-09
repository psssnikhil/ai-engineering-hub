---
title: Topic Resources — Multimodal AI & Vision-Language Models (VLMs)
description: Curated research papers, YouTube videos, open-source repositories, and code references for Vision-Language Models (VLMs), CLIP, LLaVA, Audio/Video Transformers, and Multimodal RAG.
---

# 👁️ Multimodal AI & Vision-Language Models — Topic Resources

Curated collection of landmark research papers, open-source repositories, YouTube videos, free masterclasses, and code references for **Vision-Language Models (VLMs), Contrastive Representation (CLIP), Audio/Speech Models, Video Understanding, and Multimodal RAG**.

---

## 📄 Landmark Papers & Essential Reading

| Paper / Reference | Authors / Year | Key Takeaways & Focus | Link |
|-------------------|----------------|-----------------------|------|
| **Learning Transferable Visual Models From Natural Language Supervision (CLIP)** | Radford et al. (OpenAI, 2021) | Introduced joint vision-text embedding pre-training using contrastive loss over 400M image-text pairs. | [ArXiv Link](https://arxiv.org/abs/2103.00020) |
| **Visual Instruction Tuning (LLaVA)** | Liu et al. (2023) | Combines CLIP vision encoder with LLaMA LLM via a linear projection layer trained on synthetic multimodal instruction data. | [ArXiv Link](https://arxiv.org/abs/2304.08485) |
| **Flamingo: a Visual Language Model for Few-Shot Learning** | Alayrac et al. (DeepMind, 2022) | Pioneered cross-attention layers connecting frozen vision encoders to frozen language models for zero/few-shot video & image tasks. | [ArXiv Link](https://arxiv.org/abs/2204.14198) |
| **Gemini: A Family of Highly Capable Multimodal Models** | Team Gemini (Google, 2023) | Native multimodal pre-training across text, vision, audio, and video with long-context window processing. | [ArXiv Link](https://arxiv.org/abs/2312.11805) |
| **Robust Speech Recognition via Large-Scale Weak Supervision (Whisper)** | Radford et al. (OpenAI, 2022) | Encoder-decoder Transformer model trained on 680k hours of multilingual speech for robust ASR and translation. | [ArXiv Link](https://arxiv.org/abs/2212.04356) |
| **ColPali: Efficient Document Retrieval with Vision Language Models** | Fuyu / ColPali Team (2024) | Replaces complex OCR and PDF parsing pipelines by indexing page screenshot embeddings directly using ColBERT late-interaction. | [ArXiv Link](https://arxiv.org/abs/2407.01449) |

---

## 💻 Top Open-Source Frameworks & Repositories

| Repository | Focus Area | Description | Link |
|------------|------------|-------------|------|
| **[LLaVA](https://github.com/haotian-liu/LLaVA)** | Vision-Language Models | Open-source flagship codebase for LLaVA visual instruction tuning and inference. | [GitHub Repo](https://github.com/haotian-liu/LLaVA) |
| **[Qwen2-VL](https://github.com/QwenLM/Qwen2-VL)** | Open VLM Benchmark Lead | State-of-the-art open vision-language model supporting dynamic resolution images and long videos. | [GitHub Repo](https://github.com/QwenLM/Qwen2-VL) |
| **[vLLM (Multimodal Support)](https://github.com/vllm-project/vllm)** | High-Throughput VLM Serving | vLLM engine support for multi-image, video, and text inference with PagedAttention. | [GitHub Repo](https://github.com/vllm-project/vllm) |
| **[whisper.cpp](https://github.com/ggerganov/whisper.cpp)** | High-Performance Speech C++ | High-performance C/C++ port of OpenAI's Whisper model running locally on Apple Silicon & CPU/GPU. | [GitHub Repo](https://github.com/ggerganov/whisper.cpp) |
| **[byaldi / ColPali](https://github.com/AnswerDotAI/byaldi)** | Vision Document RAG | Library for indexing PDF pages visually without text extraction using ColPali embeddings. | [GitHub Repo](https://github.com/AnswerDotAI/byaldi) |

---

## 🎥 Must-Watch YouTube Videos & Free Lectures

| Video / Playlist | Creator | Description | Link |
|------------------|---------|-------------|------|
| **CLIP Code & Architecture PyTorch Walkthrough** | Umar Jamil | Step-by-step PyTorch code walkthrough of CLIP contrastive loss, image encoder, and text encoder. | [Search on YouTube →](https://www.youtube.com/results?search_query=Umar+Jamil+CLIP+Code+%26+Architecture+PyTorch+Walkthrough) |
| **LLaVA & Vision-Language Model Architectures** | Umar Jamil | Detailed architectural breakdown of LLaVA vision projections, vicuna LLM integration, and visual tuning. | [Search on YouTube →](https://www.youtube.com/results?search_query=Umar+Jamil+LLaVA+%26+Vision-Language+Model+Architectures) |
| **Multimodal RAG with ColPali & VLM Embeddings** | Answer.AI / James Briggs | Hands-on video tutorial showing how to retrieve PDF pages visually without OCR errors. | [Search on YouTube →](https://www.youtube.com/results?search_query=Answer.AI+%2F+James+Briggs+Multimodal+RAG+with+ColPali+%26+VLM+Embeddings) |
| **Stanford CS231n: Deep Learning for Computer Vision** | Stanford University | Complete lecture series covering CNNs, Vision Transformers (ViT), and multimodal image understanding. | [Course Site](https://cs231n.stanford.edu/) |

---

## ⚙️ Code References & Hands-on Notebooks

- **[Hugging Face VLM Cookbook](https://huggingface.co/learn/vlm-cookbook/index)** — Fine-tuning LLaVA and Qwen2-VL using TRL and SFT Trainer.
- **[ColPali PDF Indexing Notebook](https://github.com/AnswerDotAI/byaldi/tree/main/examples)** — Complete Python notebook indexing document PDFs visually for RAG.
- **[Whisper PyTorch Transcription Recipes](https://github.com/openai/whisper/tree/main/notebooks)** — Audio chunking, alignment, and multi-language transcription.
