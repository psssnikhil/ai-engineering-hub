---
title: AI Engineering Coding Rounds
description: Real-world implement-from-scratch coding questions for AI/ML Engineer interviews with Python solutions
---

# AI Engineering Coding Rounds

In AI/ML Engineer interviews, coding rounds assess your ability to implement core algorithms and production patterns **from scratch in clean Python / PyTorch** — without relying on high-level abstractions like LangChain or LlamaIndex.

---

## The 6 Canonical Interview Coding Problems

Below are worked, production-grade solutions to the most frequently asked AI engineering live coding questions.

---

### Problem 1: Scaled Dot-Product Attention (PyTorch / NumPy)

**Prompt:** *"Implement scaled dot-product attention from scratch given Query \(Q\), Key \(K\), Value \(V\), and an optional causal mask."*

```python
import torch
import torch.nn as nn
import math

def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Q: [batch_size, num_heads, seq_len, d_k]
    K: [batch_size, num_heads, seq_len, d_k]
    V: [batch_size, num_heads, seq_len, d_v]
    mask: Optional tensor broadcastable to [batch_size, num_heads, seq_len, seq_len]
    """
    d_k = Q.size(-1)
    
    # 1. Compute raw attention scores: (Q @ K^T) / sqrt(d_k)
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
    
    # 2. Apply causal/padding mask (fill masked positions with -inf before softmax)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
        
    # 3. Softmax along the last dimension (keys)
    attn_weights = torch.softmax(scores, dim=-1)
    
    # 4. Multiply by values
    output = torch.matmul(attn_weights, V)
    
    return output, attn_weights

# --- Quick Test ---
batch_size, num_heads, seq_len, d_k = 2, 4, 8, 64
Q = torch.randn(batch_size, num_heads, seq_len, d_k)
K = torch.randn(batch_size, num_heads, seq_len, d_k)
V = torch.randn(batch_size, num_heads, seq_len, d_k)

# Upper triangular causal mask
causal_mask = torch.tril(torch.ones(seq_len, seq_len))
out, weights = scaled_dot_product_attention(Q, K, V, mask=causal_mask)
assert out.shape == (2, 4, 8, 64)
print("✓ Scaled dot-product attention verified.")
```

---

### Problem 2: Tool-Calling ReAct Agent Loop (Pure Python)

**Prompt:** *"Implement a ReAct (Reason + Act) agent loop that executes tool functions, parses JSON action payloads, appends observations to state, and terminates upon reaching a final answer or max iterations."*

```python
import json

class AgentLoop:
    def __init__(self, model_fn, tools, max_turns=5):
        self.model_fn = model_fn
        self.tools = {t["name"]: t["func"] for t in tools}
        self.max_turns = max_turns

    def run(self, user_query: str) -> str:
        messages = [{"role": "user", "content": user_query}]
        
        for turn in range(self.max_turns):
            response = self.model_fn(messages)
            messages.append({"role": "assistant", "content": response})
            
            # Check if model emitted tool call
            if "Action:" in response:
                try:
                    action_str = response.split("Action:")[1].strip()
                    action_data = json.loads(action_str)
                    tool_name = action_data["name"]
                    tool_args = action_data.get("args", {})
                    
                    if tool_name in self.tools:
                        result = self.tools[tool_name](**tool_args)
                        observation = f"Observation: {json.dumps(result)}"
                    else:
                        observation = f"Observation: Error: Tool '{tool_name}' not found."
                except Exception as e:
                    observation = f"Observation: Error parsing action: {str(e)}"
                    
                messages.append({"role": "user", "content": observation})
            elif "Final Answer:" in response:
                return response.split("Final Answer:")[1].strip()
                
        return "Error: Maximum agent iterations reached without final answer."
```

---

### Problem 3: Asynchronous Rate-Limited Client with Exponential Backoff

**Prompt:** *"Write a Python async API caller that enforces max concurrency (e.g. 5 parallel calls) and retries on 429 / 5xx errors with exponential backoff and jitter."*

```python
import asyncio
import random
import time

async def fetch_with_retry(api_fn, request_data, max_retries=4, base_delay=1.0):
    for attempt in range(max_retries):
        try:
            return await api_fn(request_data)
        except Exception as err:
            if attempt == max_retries - 1:
                raise err
            # Exponential backoff + full jitter
            delay = (base_delay * (2 ** attempt)) + random.uniform(0, 0.5)
            await asyncio.sleep(delay)

async def batch_process(requests, api_fn, concurrency_limit=5):
    semaphore = asyncio.Semaphore(concurrency_limit)
    
    async def worker(req):
        async with semaphore:
            return await fetch_with_retry(api_fn, req)
            
    return await asyncio.gather(*(worker(req) for req in requests))
```

---

## Ground Rules Interviewers Watch For

1. **No Framework Crutches**: Write tool dispatch, prompt formatting, and state management using plain Python primitives (`dict`, `list`, `dataclass`).
2. **Robust Exception Handling**: Handle malformed JSON, missing arguments, API rate limits, and network timeouts.
3. **Clean Code & Type Hints**: Add standard Python type hints (`List[Dict[str, Any]]`) and explicit docstrings.