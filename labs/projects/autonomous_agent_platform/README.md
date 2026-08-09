# Reference Project 2: Autonomous Agent Platform

An autonomous ReAct research agent platform with multi-step goal decomposition, standardized multi-provider LLM gateways (OpenAI + Anthropic), tool execution, and executive markdown report generation.

## Architecture

- `tools.py`: Tool definitions (web search, safe math calculation, report synthesizer) & OpenAI JSON function schemas.
- `agent.py`: Autonomous ReAct reasoning loop with step tracing & multi-provider LLM Gateway integration.
- `main.py`: Interactive CLI entry point.
- `labs.common.gateway`: Pluggable Multi-Provider LLM Gateway.

## Quick Start

```bash
cd labs/projects/autonomous_agent_platform
pip install -r requirements.txt
export OPENAI_API_KEY="sk-..."

python -m labs.projects.autonomous_agent_platform.main
```
