"""
Autonomous Agent Platform (Main Entry)
======================================
AI Engineering Hub — Reference Project 2

Usage:
  python main.py
"""

from .agent import AutonomousAgent


def main():
    print("=" * 60)
    print("  Autonomous Agent Platform (Reference Project 2)")
    print("=" * 60 + "\n")

    agent = AutonomousAgent()
    goal = "Research Model Context Protocol (MCP) and generate an executive summary report."
    print(f"User Goal: {goal}\n")

    result = agent.run(goal)

    print("\n" + "=" * 60)
    print(f"  Final Report Output (Generated via {result.get('provider_used')})")
    print("=" * 60 + "\n")
    print(result.get("final_report", result.get("final_answer")))


if __name__ == "__main__":
    main()
