# Agent System Design Interviews

The signature round for agent-engineering roles. You'll be asked to design an agentic system end to end and defend the trade-offs.

## The framework (use this every time)

1. **Clarify the task envelope** — what does the agent do, how autonomous, what's the blast radius of a mistake?
2. **The loop** — model → tool calls → observations → repeat. Define the stop conditions first.
3. **Tools** — which tools, schemas, error handling, sandboxing.
4. **Context & memory** — what goes in the window each turn; summarization/compaction strategy; persistent memory.
5. **Orchestration** — single agent vs sub-agents; when to fan out.
6. **Evals & observability** — how you know it works; traces, success metrics, regression suite.
7. **Safety & cost** — permissioning, human-in-the-loop gates, token budgets.

## Practice prompts

- Design a coding agent that fixes failing CI on a large monorepo.
- Design a customer-support agent with access to refunds (irreversible actions!).
- Design a research agent that produces a cited report from the live web.
- Design the eval harness for any of the above.

## Deep material in the handbook

- [The Agent Loop](../agent-engineering/01-agent-loop.md)
- [Memory Systems](../agent-engineering/02-memory.md)
- [Tools & MCP](../agent-engineering/03-tools-and-mcp.md)
- [Orchestration](../agent-engineering/05-orchestration.md)
- [Agent Evals](../agent-engineering/07-agent-evals.md)

--8<-- "scaffold-note.md"