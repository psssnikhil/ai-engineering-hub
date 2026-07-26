# Coding Rounds

Implement-from-scratch exercises that show up in AI engineering coding interviews.

## The canonical set

1. **Scaled dot-product attention** in NumPy/PyTorch (then multi-head).
2. **A minimal agent loop** — model call, tool dispatch, observation, stop condition (~100 lines).
3. **A RAG pipeline** — chunk, embed, retrieve top-k with cosine similarity, stuff the prompt.
4. **A simple eval harness** — run N cases, LLM-as-judge scoring, report pass rate.
5. **Streaming token handling** — parse partial tool-call JSON from a stream.
6. **A rate-limited async client** with retries and exponential backoff.

## Ground rules interviewers watch for

- Can you write the API-calling code without a framework (no LangChain crutch)?
- Do you handle malformed model output (bad JSON, refusals) gracefully?
- Do you know what to log for debugging an agent trace?

Practice against the [exercises](../exercises/index.md) and the [Build These First projects](../projects/build-these.md).

*Status: scaffold — reference solutions coming. [Contribute](../contribute.md).*
