---
title: Evals & Production — Interview Questions
description: Eval design, cost, latency, safety, and incident-response questions with model answers
---

# Evals & Production — Interview Questions

Related lessons: [LLM Evaluation & Quality](../production/module-19-llm-evaluation-quality/index.md), [LLMOps & Production Systems](../production/module-10-llmops-production-systems/index.md), [AI Safety & Ethics](../production/module-16-ai-safety-ethics/index.md).

### Q1 (L1): Why can't you just use accuracy against a golden answer set to evaluate an open-ended LLM feature?

**Short answer:** Most LLM outputs (summaries, explanations, agent plans) have many
valid phrasings, so exact-match accuracy against a single golden answer massively
undercounts correct responses; you need similarity- or criteria-based scoring instead.

**Likely follow-up:** What would you use instead? — Answer: depends on the task —
structured/extractive tasks (classification, entity extraction) can still use exact or
near-exact match; open-ended generation needs either reference-based similarity metrics
(with known limitations) or rubric-based LLM-judge scoring against explicit criteria
(faithfulness, relevance, completeness), ideally validated against human ratings on a
sample before trusting it at scale.

### Q2 (L2): What is an LLM-as-judge eval, and what's the main risk in using one?

**Short answer:** An LLM-as-judge eval uses a (usually stronger) LLM to score another
model's outputs against a rubric, instead of requiring human raters for every sample; the
main risk is that the judge inherits biases and blind spots that can silently correlate
with the system being judged, giving misleadingly consistent-looking but wrong scores.

Known judge biases include position bias (favoring the first or second response in a
pairwise comparison regardless of content), verbosity bias (favoring longer answers even
when not better), and self-preference bias (a judge favoring outputs that match its own
model family's style). If the same model family is used to both generate and judge, these
biases compound. The mitigation isn't to avoid LLM judges entirely — human eval at scale
is often infeasible — but to validate the judge against a sample of human ratings
(measure agreement rate), use structured rubrics rather than open-ended "is this good?"
prompts, and periodically re-validate as the judged system changes.

**Likely follow-up:** How would you detect if your LLM judge has drifted or become
unreliable over time? — Answer: maintain a small held-out set with human labels and
periodically re-run the judge against it, tracking agreement rate over time; a drop
signals the judge (or the underlying model version behind it) needs re-calibration or the
rubric needs tightening.

*See also: [LLM Evaluation & Quality](../production/module-19-llm-evaluation-quality/index.md)*

### Q3 (L2): Your p50 latency looks fine but users are complaining about slowness. What do you check first?

**Short answer:** Check the tail latency distribution (p95/p99), not just the median —
user-perceived slowness is usually driven by a subset of requests hitting a much worse
path (cold cache, retry, rate-limit backoff, long-tail prompt/output length), which a p50
number completely hides.

Beyond percentiles, break latency down by stage: time-to-first-token vs total generation
time (a fast TTFT with slow total generation still *feels* slow for long outputs; users
notice differently depending on whether output is streamed), and check whether the slow
requests correlate with a specific cause — longer input/output token counts, retries due
to transient errors, a specific model/provider region, or contention (are p99 spikes
correlated with traffic spikes, suggesting a capacity/batching issue rather than a
per-request issue).

**Likely follow-up:** If p99 latency is 8x p50, is that necessarily a problem? — Answer:
not automatically — some tail inflation is expected from naturally longer requests (a
5,000-token generation will always take longer than a 50-token one); the question is
whether the tail is explained by *request characteristics* (fine) or by *infrastructure
behavior* like queueing, retries, or cold starts (a real problem), which you determine by
conditioning the percentile breakdown on request size.

### Q4 (L2): How do you decide whether a cost increase from switching to a larger/more expensive model is justified?

**Short answer:** Run an eval-driven comparison — measure the quality delta on your
actual task distribution (not a generic benchmark), multiply by the business value of
that quality delta (e.g. reduced escalation rate, higher task success rate), and compare
against the incremental cost at your expected volume; "the bigger model scores higher on
a public leaderboard" is not sufficient justification on its own.

**Likely follow-up:** What's a cheaper alternative to always using the larger model if
only some requests need it? — Answer: a routing/cascade strategy — send requests to a
cheaper/smaller model first, and escalate to the larger model only when a confidence
signal (low logprob, a lightweight classifier, or an explicit "I'm not sure" self-report)
suggests the smaller model is likely to fail, capturing most of the quality benefit at a
fraction of the average cost.

### Q5 (L3): Design an incident-response process for "the model started giving factually wrong answers in production" — what do you actually do in the first hour?

**Short answer:** First isolate scope and cause category (model/provider change vs
data/retrieval change vs prompt change vs traffic pattern change) using recent deploys
and version pins as the primary signal, then decide between mitigation (rollback,
disable the feature, fall back to a cached/safe response) and root-cause fixing —
mitigate first, root-cause after, since production correctness incidents compound the
longer they run.

Concretely: check what changed recently — a silent model version update from a provider
(if you're not pinning versions), a prompt or system-message change, a retrieval index
update, or a new class of user input the system wasn't tested against. Check whether the
issue is uniform (all requests affected — points to a global change like model/prompt) or
segmented (only certain query types or a certain retrieval source — points to a data or
retrieval issue). If a specific recent deploy correlates, roll it back first and confirm
recovery before doing a deeper root-cause investigation — don't debug in production while
users are actively getting wrong answers if a safe rollback path exists. Add or check
alerting on the metric that should have caught this before users did (e.g. a faithfulness
score dropping, an unusual spike in a specific answer pattern) as a same-incident
follow-up.

**Likely follow-up:** How do you prevent "silent" model version changes from being the
cause next time? — Answer: pin exact model versions in production rather than tracking
"latest," and treat any model version bump as a deploy that goes through the same eval
gate as a prompt or code change before rolling out.

### Q6 (L3): How would you design guardrails for a customer-facing agent that can take real actions (e.g. issue refunds), balancing safety against usefulness?

**Short answer:** Tier actions by blast radius and reversibility — fully autonomous for
low-risk/reversible actions, human-in-the-loop confirmation for medium-risk actions, and
hard-blocked (never agent-executable) for high-risk/irreversible ones — rather than a
single global "always confirm" or "never confirm" policy.

A single policy in either direction fails: always requiring human confirmation defeats
the purpose of automation and creates approval fatigue where humans start
rubber-stamping without real review; never requiring confirmation risks large-blast-radius
mistakes (e.g. a $50,000 refund typo) going out unchecked. A tiered policy — e.g. refunds
under $20 auto-approved with post-hoc audit logging, refunds $20-$500 require a
lightweight confirmation step, refunds over $500 or any account-deletion-class action
require explicit human approval with full context shown — matches oversight cost to
actual risk. This also needs enforcement *outside* the model's own judgment: the dollar
thresholds and action classes should be enforced by the tool/API layer (hard limits the
agent literally cannot exceed via a tool call), not just instructed via prompt, since
prompt-level instructions can fail under injection or model error.

**Likely follow-up:** Why enforce limits at the tool/API layer instead of trusting the
model to follow prompted limits? — Answer: prompt instructions are a soft constraint —
they can be overridden by injection, degraded by context length, or simply gotten wrong
by the model; a hard limit enforced in the tool implementation (e.g. the refund API
itself rejects amounts over the threshold without a separate approval token) fails safe
regardless of what the model outputs, which is the property you actually need for a
real financial or safety guardrail.

*See also: [AI Safety & Ethics](../production/module-16-ai-safety-ethics/index.md)*
