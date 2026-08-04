---
title: LLM & Transformer Fundamentals — Interview Questions
description: Attention, tokenization, training dynamics, and sampling questions with model answers
---

# LLM & Transformer Fundamentals — Interview Questions

Related lessons: [Transformers & Attention](../foundations/module-06-transformers-attention-mechanisms/index.md), [Large Language Models](../foundations/module-07-large-language-models-llms/index.md), [Attention Math deep dive](../deep-dives/attention-math.md).

### Q1 (L1): Why does self-attention scale by \( \sqrt{d_k} \)?

**Short answer:** Without scaling, the dot products \( QK^T \) grow with the dimension
\( d_k \), pushing softmax into a regime where gradients vanish.

As \( d_k \) grows, the dot product of two random vectors has variance proportional to
\( d_k \) (each of the \( d_k \) terms adds independent variance). Large-magnitude
logits saturate softmax — one entry approaches 1 and the rest approach 0 — which kills
the gradient signal needed for training. Dividing by \( \sqrt{d_k} \) keeps the variance
of the dot product roughly constant at 1 regardless of dimension, keeping softmax in its
sensitive range.

**Likely follow-up:** What breaks if you use a fixed learning rate but double \( d_k \)
without this scaling? — Answer: the pre-softmax logits get larger, softmax becomes
near one-hot early in training, and the effective learning signal for attention weights
collapses; training becomes much slower or unstable even though the model has more
capacity.

!!! warning "Common wrong answer"
    "It's just a normalization trick, like batch norm." This misses *why* — it's not
    normalizing activations across a batch, it's counteracting a specific
    dimensionality-dependent variance blowup in the dot product itself.

### Q2 (L1): What's the difference between BPE, WordPiece, and byte-level BPE tokenization?

**Short answer:** All three are subword tokenizers that build a vocabulary from
frequently co-occurring character sequences; they differ in the merge criterion and the
base alphabet.

BPE merges the most *frequent* adjacent pair repeatedly. WordPiece (BERT) merges the
pair that most increases the *likelihood* of the training corpus under a unigram
language model, which tends to favor merges that are more linguistically meaningful.
Byte-level BPE (GPT-2 onward) operates on raw UTF-8 bytes instead of Unicode characters
as the base alphabet, so it can represent *any* input — emoji, unseen scripts — without
an `<unk>` token, at the cost of every non-ASCII character costing more tokens.

**Likely follow-up:** Why does this make non-English text more expensive to run through
GPT-family models? — Answer: byte-level BPE vocabularies are trained mostly on
English-heavy corpora, so common English words get single-token merges while other
scripts (e.g. Hindi, Chinese) fall back to multi-byte sequences per character, inflating
token count and therefore cost and effective context window for the same amount of text.

*See also: [Tokenization internals](../deep-dives/tokenization-internals.md)*

### Q3 (L2): Explain KV-caching and why it doesn't help the prefill phase.

**Short answer:** KV-caching stores the key and value projections for all previously
generated tokens so each new decoding step only computes attention for the one new
token, instead of recomputing it for the whole sequence.

During autoregressive decoding, generating token \( t \) needs attention over tokens
\( 1..t \). Without caching, that means recomputing \( K \) and \( V \) for the entire
prefix at every step — \( O(n^2) \) work across a generation of length \( n \). Caching
turns each step into \( O(n) \) work (attend to cached \( K, V \) plus one new
projection), making total generation \( O(n^2) \) still, but with a much smaller
constant and no redundant matrix multiplies. Prefill (processing the prompt) doesn't
benefit because every prompt token's \( K, V \) is being computed for the *first* time —
there's nothing to cache yet, so prefill is compute-bound and parallelizable, while
decoding is memory-bandwidth bound (moving the growing cache in and out of memory each
step).

**Likely follow-up:** Why is decode phase throughput at high concurrency dominated by
memory bandwidth, not FLOPs? — Answer: each decode step does very little compute per
token (one matmul-ish pass) but must read the entire KV cache for every sequence in the
batch from HBM; at scale the GPU spends more time moving cache bytes than computing,
which is exactly what techniques like PagedAttention and grouped-query attention target.

!!! warning "Common wrong answer"
    "KV-cache speeds up the whole forward pass." It specifically speeds up *decoding*
    (autoregressive generation) by avoiding recomputation of past tokens' keys/values —
    it doesn't change the complexity of a single non-cached forward pass.

### Q4 (L2): Why does increasing temperature increase output diversity, and why can it also increase hallucination?

**Short answer:** Temperature \( T \) rescales the logits before softmax
(\( \text{softmax}(z/T) \)); as \( T \) increases, the probability distribution
flattens, so lower-probability (less confident) tokens become more likely to be sampled.

At \( T \to 0 \), sampling approaches greedy decoding — always the highest-probability
token. At \( T = 1 \), you sample from the model's raw distribution. At \( T > 1 \), you
actively boost the odds of tokens the model considered less likely, which increases
lexical diversity but also increases the odds of picking a token that leads down a path
the model has less evidence for — a factual claim it's not well-calibrated on. This is
why temperature and hallucination correlate: you're deliberately sampling further from
the model's most-confident continuation.

**Likely follow-up:** How would you choose temperature differently for a code-generation
task vs a creative-writing task? — Answer: code generation wants low temperature (0-0.3)
since there's usually one syntactically/semantically correct continuation and diversity
mostly introduces bugs; creative writing benefits from higher temperature (0.7-1.0) since
multiple continuations are valid and diversity is the point.

### Q5 (L2): What is the difference between pretraining, SFT, and RLHF/DPO, and what failure mode does each stage primarily fix?

**Short answer:** Pretraining teaches broad language modeling from raw text; SFT teaches
instruction-following format from curated (prompt, response) pairs; RLHF/DPO aligns
outputs to human preference beyond what SFT data alone captures.

A raw pretrained model is a strong next-token predictor but has no notion of "answer this
instruction helpfully" — prompted with a question, it might continue with more questions
(that's what its training distribution looked like). SFT fixes this by fine-tuning on
demonstration data showing the instruction → response format, producing a model that
*attempts* to be helpful but is still calibrated to imitate the SFT dataset's style and
quality, including its blind spots. RLHF (reward model + PPO) or DPO (direct preference
optimization, no separate reward model or RL loop) then optimize the policy against
*preference* signal — which of two responses a human (or preference model) prefers —
which can push the model toward qualities that are easy to prefer but hard to
demonstrate directly, like conciseness, refusal calibration, and avoiding subtly wrong
confident answers.

**Likely follow-up:** Why has DPO become popular relative to full RLHF? — Answer: DPO
reformulates the RLHF objective as a single classification-style loss over preference
pairs, removing the need for a separately trained reward model and an unstable PPO loop,
which makes it materially cheaper and more stable to run at the cost of some flexibility
(e.g. no online reward shaping during training).

!!! warning "Common wrong answer"
    "RLHF makes the model smarter." It doesn't add capability — the pretrained model
    already has the underlying knowledge; RLHF/DPO reshape *which* of the capable
    model's outputs get surfaced.

### Q6 (L3): Why do larger context windows not automatically mean the model uses all of that context well, and how would you test this?

**Short answer:** Attention is not free — longer contexts dilute attention weight across
more tokens, and models trained on limited long-context examples often exhibit a
"lost in the middle" effect, where information at the start and end of context is
retrieved more reliably than information buried in the middle.

This is an empirical, not just theoretical, claim: needle-in-a-haystack evaluations
(placing a specific fact at varying depths in a long context and asking the model to
retrieve it) consistently show accuracy dips for mid-document placement in many models,
even when the raw context window is large enough to fit the fact. The cause is a mix of
training data distribution (long-context training examples are rarer and often have
answer-relevant content near the edges) and positional encoding behavior at long
distances (e.g. RoPE's rotary embeddings degrade at positions far outside the training
distribution without extrapolation techniques like NTK-aware scaling or YaRN).

**Likely follow-up:** If you had a document too large for even a 1M-token context
window, would you prefer long-context or RAG? — Answer: it depends on the access
pattern — long-context is better when the task genuinely needs to reason *across* most
of the document (e.g. summarization, cross-referencing), while RAG is better when only a
small, query-dependent subset of the document is relevant per query, since retrieval
avoids paying the latency/cost of processing irrelevant tokens and sidesteps
lost-in-the-middle entirely by narrowing what's in context.

*See also: [Large Language Models](../foundations/module-07-large-language-models-llms/index.md)*

### Q7 (L3): Explain the difference between grouped-query attention (GQA) and multi-head attention (MHA), and the tradeoff GQA makes.

**Short answer:** MHA gives every attention head its own \( K \) and \( V \)
projections; GQA shares one set of \( K, V \) projections across a group of query heads,
shrinking the KV cache proportionally to the group size at a small quality cost.

The KV cache size scales with `num_kv_heads × head_dim × sequence_length` — for MHA that
equals the number of query heads, but for GQA it's divided by the group size (e.g. 8
query heads sharing 2 KV heads means a 4x smaller cache). Since decode-phase throughput
is memory-bandwidth bound on moving the KV cache (see Q3), shrinking it directly
increases achievable batch size and throughput at serving time. The tradeoff is that
multiple query heads now attend using the same keys/values, reducing the model's
representational flexibility slightly — in practice, well-tuned GQA models (e.g. Llama 2
70B) show negligible quality loss versus MHA for a large serving efficiency win, which is
why GQA (and its extreme, multi-query attention with one shared KV head) has become
standard in production LLMs.

**Likely follow-up:** Where does GQA sit on the spectrum between MHA and MQA
(multi-query attention), and why would you pick a middle ground? — Answer: MQA (one KV
head total) maximizes cache savings but has the largest quality risk since *all* query
heads share one key/value representation; GQA with a moderate group count (e.g. 8 groups
for 64 heads) captures most of the throughput win while preserving enough per-group
representational diversity to avoid the quality cliff MQA can show on some tasks.
