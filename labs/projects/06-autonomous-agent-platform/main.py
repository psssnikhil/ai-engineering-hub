"""
Autonomous Agent Platform (Main Entry)
======================================
AI Engineering Hub — Reference Project 06

Usage:
  python main.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

try:
    from agent import AutonomousAgent
except ImportError:
    from .agent import AutonomousAgent


def main():
    print("=" * 60)
    print("  Autonomous Agent Platform (Project 06)")
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
