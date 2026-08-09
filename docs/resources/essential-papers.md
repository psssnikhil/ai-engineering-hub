---
title: Essential Papers
---

# Essential Papers

Curated papers every AI engineer should know — not an exhaustive dump. For the full auto-index see [Papers](papers.md).

## Foundations

| Paper | Why it matters | Module |
|-------|----------------|--------|
| [Attention Is All You Need](https://arxiv.org/abs/1706.03762) (Vaswani et al.) | Transformer architecture | [M00](../foundations/module-00-genai-foundations-from-nlp-to-transformers/index.md), [M06](../foundations/module-06-transformers-attention-mechanisms/index.md) |
| [BERT](https://arxiv.org/abs/1810.04805) | Bidirectional pre-training | M00 |
| [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) (GPT-3) | In-context learning | [M07](../foundations/module-07-large-language-models-llms/index.md) |
| [FlashAttention](https://arxiv.org/abs/2205.14135) (Dao et al.) | IO-aware GPU attention | M06, [M10](../production/module-10-llmops-production-systems/index.md) |

## Reasoning & RL

| Paper | Why it matters | Module |
|-------|----------------|--------|
| [DeepSeek-R1](https://arxiv.org/abs/2501.12948) (DeepSeek AI) | Pure RL reasoning & CoT | M07 |
| [Process Reward Models](https://arxiv.org/abs/2305.20050) (OpenAI) | Step-by-step verification | M07 |
| [Tree of Thoughts](https://arxiv.org/abs/2305.04091) (Yao et al.) | MCTS search with LLMs | M07, M11 |

## RAG & retrieval

| Paper | Why it matters | Module |
|-------|----------------|--------|
| [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401) | RAG foundation | [M09](../build/module-09-rag-retrieval-augmented-generation/index.md) |
| [Dense Passage Retrieval](https://arxiv.org/abs/2004.04906) | Dense retrieval | M09, [M13](../build/module-13-vector-databases-deep-dive/index.md) |
| [ColBERT](https://arxiv.org/abs/2004.12832) (Khattab et al.) | Late interaction retrieval | M09, M13 |

## Agents & Code Intelligence

| Paper | Why it matters | Module |
|-------|----------------|--------|
| [ReAct](https://arxiv.org/abs/2210.03629) | Reason + act loop | [M11](../build/module-11-ai-agents-fundamentals/index.md) |
| [Toolformer](https://arxiv.org/abs/2302.04761) | Self-supervised tool use | M11, [M18](../build/module-18-agent-harness-tools-runtime/index.md) |
| [SWE-bench](https://arxiv.org/abs/2310.06770) | Coding agent benchmark | M11, M18 |

## Fine-Tuning & Alignment

| Paper | Why it matters | Module |
|-------|----------------|--------|
| [LoRA](https://arxiv.org/abs/2106.09685) (Hu et al.) | Parameter-efficient tuning | [M15](../advanced/module-15-fine-tuning-custom-models/index.md) |
| [Direct Preference Optimization (DPO)](https://arxiv.org/abs/2305.18290) | Reference-based alignment | M15 |
| [GRPO](https://arxiv.org/abs/2402.03300) (DeepSeek) | Group relative RL alignment | M15 |

## Evaluation & safety

| Paper | Why it matters | Module |
|-------|----------------|--------|
| [vLLM / PagedAttention](https://arxiv.org/abs/2309.06180) | Virtual memory serving | [M10](../production/module-10-llmops-production-systems/index.md) |
| [HELM](https://arxiv.org/abs/2211.09110) | Holistic LLM benchmarking | [M19](../production/module-19-llm-evaluation-quality/index.md) |
| [Judging LLM-as-a-Judge](https://arxiv.org/abs/2306.05685) (MT-Bench) | LLM judges | M19 |
| [Constitutional AI](https://arxiv.org/abs/2212.08073) | RLHF alternative | [M16](../production/module-16-ai-safety-ethics/index.md) |

## Visual companion

- [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) — Jay Alammar (open educational)
