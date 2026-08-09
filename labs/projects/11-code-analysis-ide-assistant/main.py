"""
Project 11: Code Analysis & IDE Assistant
=========================================
Domain: Developer Tools & IDE Coding Assistants

A developer tool copilot featuring:
1. Python AST Codebase Structure Parser & Function Indexing
2. Security Vulnerability & Hardcoded Secret Detector
3. Refactoring & Unit Test Generation Pipeline

Usage:
  python main.py
"""

import ast
import os
import sys
import json
from dataclasses import dataclass
from typing import Dict, Any, List, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from labs.common.gateway import LLMGateway


SAMPLE_CODEBASE = """
import os
import sqlite3

def query_user_data(user_input):
    # Potential SQL Injection vulnerability
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + user_input + "'"
    cursor.execute(query)
    return cursor.fetchall()

def compute_factorial(n):
    if n <= 1:
        return 1
    return n * compute_factorial(n - 1)
"""


class CodeASTParser:
    """Parses Python source code into AST trees to extract functions and vulnerability warnings."""

    @staticmethod
    def analyze_source(code: str) -> Dict[str, Any]:
        tree = ast.parse(code)
        functions = []
        vulnerabilities = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append({"name": node.name, "line": node.lineno})
            elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
                # Simple heuristic for string concatenation in SQL queries
                vulnerabilities.append("Warning: String concatenation detected in binary operation (potential SQL injection risk).")

        return {
            "functions_found": functions,
            "vulnerability_alerts": list(set(vulnerabilities))
        }


class IDECodingAssistant:
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()
        self.ast_parser = CodeASTParser()

    def analyze_and_refactor(self, source_code: str) -> Dict[str, Any]:
        # Step 1: Run AST analysis
        ast_results = self.ast_parser.analyze_source(source_code)

        # Step 2: Query LLMGateway for refactoring & safe query generation
        prompt = (
            f"Source Code:\n```python\n{source_code}\n```\n\n"
            f"AST Analysis Alerts:\n{json.dumps(ast_results, indent=2)}\n\n"
            "Provide a secure refactored version using parameterized SQL queries and unit tests."
        )

        messages = [
            {"role": "system", "content": "You are a Senior Security Engineer & Python IDE Assistant. Refactor code safely and suggest unit tests."},
            {"role": "user", "content": prompt}
        ]

        resp = self.gateway.generate(messages=messages, temperature=0.0)

        return {
            "ast_analysis": ast_results,
            "refactored_output": resp.content,
            "provider": resp.provider_name
        }


def main():
    print("=" * 60)
    print("  Code Analysis & IDE Assistant (Project 11)")
    print("=" * 60 + "\n")

    assistant = IDECodingAssistant()
    print("Analyzing Source Code snippet for SQL Injection vulnerabilities...")

    res = assistant.analyze_and_refactor(SAMPLE_CODEBASE)
    print(f"\nAST Analysis Alerts:\n{json.dumps(res['ast_analysis'], indent=2)}\n")
    print(f"Refactored Code & Safety Report (Generated via {res.get('provider')}):\n")
    print(res.get("refactored_output"))


if __name__ == "__main__":
    main()
