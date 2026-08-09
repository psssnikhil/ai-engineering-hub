---
title: RAG — Interview Questions
description: Chunking, retrieval, reranking, and hallucination questions with model answers
---

# RAG — Interview Questions

Related lessons: [RAG — Retrieval Augmented Generation](../build/module-09-rag-retrieval-augmented-generation/index.md), [Vector Databases](../build/module-13-vector-databases-deep-dive/index.md).

### Q1 (L1): Why does chunk size matter, and what breaks at each extreme?

**Short answer:** Chunk size trades off retrieval precision against context
completeness — too small and chunks lose the surrounding context needed to answer;
too large and irrelevant content dilutes the embedding and wastes context budget.

A chunk that's too small (e.g. one sentence) can be embedded very precisely, but if the
answer requires a fact that's split across two sentences ("The policy was updated." /
"It now requires 30 days notice."), retrieval may fetch only one half. A chunk that's
too large (e.g. a whole 10-page section) produces an embedding that's an average over
many topics, so a query about one narrow sub-topic in that section may not score highly
against it even though the answer is in there — and even if retrieved, most of the
context window is spent on irrelevant text, increasing cost and giving the model more
room to get distracted.

**Likely follow-up:** How would you choose chunk size for a legal contracts corpus vs a
customer support FAQ? — Answer: legal contracts benefit from larger, structure-aware
chunks (e.g. per-clause) since clauses reference definitions and conditions that need to
stay together for correct interpretation; FAQs benefit from small, self-contained chunks
(one Q&A pair each) since each chunk is already a complete, independent unit.

### Q2 (L1): Why is chunk overlap used, and what's the cost of using too much?

**Short answer:** Overlap prevents a fact from being split exactly at a chunk boundary
by duplicating a window of text between consecutive chunks; too much overlap inflates
index size and retrieval noise (near-duplicate chunks competing for the same top-k slots).

**Likely follow-up:** Is overlap still needed if you use semantic chunking (splitting at
natural topic boundaries) instead of fixed-size chunking? — Answer: less so — semantic
chunking already reduces the chance of splitting a coherent idea in half, so overlap can
usually be smaller or omitted, though a small overlap is still cheap insurance against
misdetected boundaries.

### Q3 (L2): Why does hybrid search (BM25 + vector) usually outperform pure vector search?

**Short answer:** Dense embeddings are good at semantic/paraphrase similarity but weak
at exact-match signals (IDs, part numbers, rare proper nouns, exact phrases) that BM25's
term-frequency scoring handles natively.

Embedding models are trained to cluster semantically similar text, which means a query
like "cancellation fee" and a document phrase "termination charge" will score highly
together even with no shared tokens — a real strength. But that same property means an
exact-match query like an invoice number, an error code, or a specific legal citation can
retrieve poorly, because the embedding space wasn't optimized to distinguish those
tokens precisely — nearby-but-wrong IDs can embed close together. BM25 (or any sparse
lexical method) directly rewards exact and near-exact term overlap, which is exactly the
signal dense retrieval is weakest on. Combining both (typically via reciprocal rank
fusion or a weighted score blend) covers both failure modes.

**Likely follow-up:** How would you tune the blend weight between BM25 and vector
scores? — Answer: empirically, on a labeled eval set of (query, relevant doc) pairs,
sweeping the blend weight and measuring recall@k / MRR; in practice many teams start
around an equal weight after score normalization and adjust based on whether the eval
set is dominated by exact-match or semantic-paraphrase queries.

!!! warning "Common wrong answer"
    "Vector search is strictly better because it 'understands meaning'." Semantic
    understanding is a strength, not a superset of lexical matching — the two methods
    fail on different query types, which is precisely why hybrid retrieval exists.

### Q4 (L2): Why can adding a reranker improve answer quality even when the retriever's recall is already high?

**Short answer:** The retriever (bi-encoder) scores query and document independently for
speed, which is a weaker relevance signal than a reranker (cross-encoder), which jointly
encodes the query and document together and can model fine-grained interactions.

A bi-encoder embeds the query and each document separately into the same vector space and
compares them with cosine similarity or dot product — this is fast (embeddings are
precomputed for the corpus, and the query is compared via nearest-neighbor search) but
loses the ability to model interactions between specific query and document tokens. A
cross-encoder reranker takes the concatenated (query, document) pair through a
transformer jointly, so it can directly attend between query terms and document terms —
much higher relevance accuracy, but too slow to run over the whole corpus. The standard
pattern is: retrieve top-k (e.g. 50-100) cheaply with the bi-encoder for recall, then
rerank that small candidate set expensively with the cross-encoder for precision, giving
you both properties.

**Likely follow-up:** What's the latency cost of adding a reranker, and how do you keep
it acceptable? — Answer: reranking k candidates costs roughly k forward passes through a
(usually smaller) cross-encoder model; teams keep this bounded by capping k (e.g. rerank
only the top 20-50 retrieved, not all retrieved), using a distilled/small reranker model,
and batching the reranker calls.

### Q5 (L2): Your RAG system answers confidently with a fact that isn't in any retrieved document. What are the possible causes, and how do you diagnose which one it is?

**Short answer:** Either retrieval failed to surface the relevant chunk (a *retrieval*
failure), or the right chunk was retrieved but the model ignored it and used parametric
knowledge instead (a *grounding* failure) — these need different fixes, so diagnosis
must separate them.

To diagnose: log the exact chunks passed to the model for that query and manually check
whether the fact is present. If it's absent, this is a retrieval problem — check
recall@k on a labeled eval set, consider hybrid search or query rewriting (the user's
phrasing may not match document phrasing). If the fact *is* present in the retrieved
context but the model still answered from memory, this is a grounding/faithfulness
problem — check the prompt (is retrieved context clearly marked as the source of truth?
is the instruction explicit about not using outside knowledge?), and consider adding a
faithfulness eval (e.g. an LLM-judge scoring whether every claim in the answer is
supported by the provided context) to catch this systematically rather than by manual
sampling.

**Likely follow-up:** How would you build an automated eval to catch this going forward
in CI? — Answer: a faithfulness/groundedness metric — for each answer, extract its
claims and check each against the retrieved context (via NLI-style entailment or an
LLM judge), and fail the eval if any claim isn't supported; run this on a held-out set of
representative queries on every prompt or retrieval-pipeline change.

*See also: [LLM Evaluation & Quality](../production/module-19-llm-evaluation-quality/index.md)*

### Q6 (L3): How would you handle a RAG corpus where documents are updated frequently (e.g. every few minutes) at scale?

**Short answer:** Separate the ingestion pipeline into incremental upsert (not full
reindex), version documents so stale chunks can be identified and invalidated, and
decouple embedding computation from index write so the two can scale independently.

Full reindexing is \( O(n) \) in corpus size and becomes infeasible as update frequency
rises relative to corpus size. Instead: on each document change, recompute embeddings
only for the changed document's chunks, and upsert (insert-or-replace) those vectors by a
stable chunk ID (e.g. `doc_id::chunk_index`) so old vectors for that document are
overwritten rather than accumulating duplicates. Track a `document_version` or
`updated_at` alongside each vector so you can detect and purge orphaned chunks (e.g. a
chunk boundary shift that leaves an old chunk 6 with no corresponding new content).
Decoupling embedding computation (CPU/GPU-bound, batchable, can queue) from the vector
index write (needs to be fast and available) lets you absorb update bursts with a queue
instead of blocking writers.

**Likely follow-up:** How do you avoid serving stale results to a query that arrives
during an in-progress update? — Answer: depends on the consistency requirement — for most
RAG use cases eventual consistency (a few seconds to minutes of staleness) is acceptable
and far cheaper than synchronous index updates; if strict consistency is required, use a
read-after-write pattern where updates append to a fast, small "recent changes" overlay
index that's checked first, merging results with the main index until the background
reindex catches up.
