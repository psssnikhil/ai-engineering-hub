# Reference Project: Autonomous Agent Platform

An autonomous ReAct research agent platform with multi-step goal decomposition, standardized multi-provider LLM gateways (OpenAI + Anthropic), tool execution, and executive markdown report synthesis.

```mermaid
flowchart TD
    Task["Complex Task Goal"] --> Planner["Planner & ReAct Loop"]
    Planner --> SearchTool["Web Search Tool"]
    Planner --> MathTool["Math Tool"]
    SearchTool & MathTool --> Synthesizer["Executive Report Synthesizer"]
    Synthesizer --> Report["Structured Markdown Report"]
```

## Quick Example Code

```python
from agent import AutonomousAgent

agent = AutonomousAgent(max_steps=6)
report = agent.run("Research market trends in AI Agents for 2026.")
print(report)
```

## Quickstart

```bash
python main.py
```
