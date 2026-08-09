"""
Project 11: Production-Grade Code Analysis & IDE Assistant
===========================================================
Domain: Developer Tools & IDE Coding Assistants

Features:
  1. AST call-graph parser: Maps function declarations and internal call invocations.
  2. AST Security Analyzer:
     - String Concatenation SQL injection checking.
     - Hardcoded API secret key regex matching.
  3. Git Unified Diff Formatter: Formats changes as standardized Git patch sets.
  4. Automation Unit Test Blueprinting: Builds runnable pytest code.
"""

import ast
import os
import sys
import json
import re
from dataclasses import dataclass
from typing import Dict, Any, List, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from labs.common.gateway import LLMGateway

# Highly vulnerable and unoptimized sample python file
SAMPLE_CODEBASE = """
import os
import sqlite3

API_TOKEN = "sk-proj-44129841289412AABBCCDDEE"

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

def run_pipeline():
    user = "alice"
    data = query_user_data(user)
    fact = compute_factorial(5)
    print(f"Fact: {fact}, Data: {data}")
"""


class CodeASTParser(ast.NodeVisitor):
    """Walks the Python Abstract Syntax Tree (AST) to build call graphs and scan for vulnerabilities."""
    def __init__(self):
        self.functions: List[Dict[str, Any]] = []
        self.call_graph: Dict[str, List[str]] = {}
        self.current_function: Optional[str] = None
        self.vulnerabilities: List[Dict[str, Any]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        fn_info = {
            "name": node.name,
            "args": [arg.arg for arg in node.args.args],
            "line": node.lineno
        }
        self.functions.append(fn_info)
        self.call_graph[node.name] = []
        
        # Track context for call graph mapping
        old_fn = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = old_fn

    def visit_Call(self, node: ast.Call):
        if self.current_function and isinstance(node.func, ast.Name):
            self.call_graph[self.current_function].append(node.func.id)
            
        # SQL Injection Check: inspect execute calls
        if isinstance(node.func, ast.Attribute) and node.func.attr == "execute":
            # Check if first argument is a binary addition string concatenation
            if node.args:
                first_arg = node.args[0]
                if isinstance(first_arg, ast.BinOp) and isinstance(first_arg.op, ast.Add):
                    self.vulnerabilities.append({
                        "type": "SQL_INJECTION_RISK",
                        "severity": "CRITICAL",
                        "line": node.lineno,
                        "description": "SQL query built using string concatenation. Use parameterized query bindings instead."
                    })
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        # Scan for hardcoded API keys/tokens in assignments
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id.lower()
                if any(x in var_name for x in ["key", "token", "secret", "password"]):
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                        val = node.value.value
                        # Check length or high-entropy pattern
                        if len(val) > 16:
                            self.vulnerabilities.append({
                                "type": "HARDCODED_SECRET",
                                "severity": "HIGH",
                                "line": node.lineno,
                                "description": f"Variable '{target.id}' appears to contain a hardcoded credential/secret key."
                            })
        self.generic_visit(node)


class IDECodingAssistant:
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()

    def generate_git_diff(self, original: str, refactored: str) -> str:
        """Formulate a Git-style patch diff between original and refactored versions."""
        import difflib
        orig_lines = original.strip().splitlines(keepends=True)
        ref_lines = refactored.strip().splitlines(keepends=True)
        
        diff = difflib.unified_diff(
            orig_lines, ref_lines,
            fromfile="original_code.py",
            tofile="secure_code.py"
        )
        return "".join(diff)

    def analyze_and_refactor(self, source_code: str) -> Dict[str, Any]:
        # Step 1: Execute local AST checks
        tree = ast.parse(source_code)
        parser = CodeASTParser()
        parser.visit(tree)

        ast_results = {
            "functions": parser.functions,
            "call_graph": {k: list(set(v)) for k, v in parser.call_graph.items()},
            "vulnerability_alerts": parser.vulnerabilities
        }

        # Step 2: Formulate prompt requesting secure refactoring and test coverage
        prompt = (
            f"Review the source code below and its structural AST warnings.\n\n"
            f"Source Code:\n```python\n{source_code}\n```\n\n"
            f"AST Analysis Results:\n{json.dumps(ast_results, indent=2)}\n\n"
            "Task:\n"
            "1. Refactor the code to fix any vulnerabilities (parameterize SQL queries, remove secrets).\n"
            "2. Output the refactored secure version in python code.\n"
            "3. Output a runnable unit test script using pytest.\n"
            "Format the response cleanly with markdown sections."
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a Senior Security Architect & Python Compiler Expert. "
                    "Provide refactored secure code blocks and separate pytest test classes."
                )
            },
            {"role": "user", "content": prompt}
        ]

        try:
            resp = self.gateway.generate(messages=messages, temperature=0.0)
            llm_text = resp.content
            provider = resp.provider_name
        except Exception as e:
            # Local fallback refactored output
            llm_text = (
                "### Refactored Secure Code:\n"
                "```python\n"
                "import os\n"
                "import sqlite3\n\n"
                "def query_user_data(user_input):\n"
                "    conn = sqlite3.connect(\"app.db\")\n"
                "    cursor = conn.cursor()\n"
                "    # Safe parameterized query bindings\n"
                "    cursor.execute(\"SELECT * FROM users WHERE username = ?\", (user_input,))\n"
                "    return cursor.fetchall()\n"
                "```"
            )
            provider = "LocalFallback"

        # Try to extract the refactored code block to build git unified diff
        refactored_code = ""
        code_match = re.search(r"```python\s*\n(.*?)\n```", llm_text, re.DOTALL)
        if code_match:
            refactored_code = code_match.group(1)

        git_diff = ""
        if refactored_code:
            git_diff = self.generate_git_diff(source_code, refactored_code)

        return {
            "ast_analysis": ast_results,
            "assistant_report": llm_text,
            "git_patch_diff": git_diff,
            "provider": provider
        }


def main():
    print("=" * 70)
    print("  IDE Code Analyzer & Secure Assistant (Project 11)")
    print("=" * 70 + "\n")

    assistant = IDECodingAssistant()
    print("Ingesting sample codebase, performing static AST parse...")
    
    result = assistant.analyze_and_refactor(SAMPLE_CODEBASE)
    
    print("\n[AST Extracted Structural Insights]:")
    print(json.dumps(result["ast_analysis"], indent=2))
    
    if result["git_patch_diff"]:
        print("\n[Generated Git Patch Diff]:")
        print("-" * 70)
        print(result["git_patch_diff"])
        print("-" * 70)

    print("\n[Refactoring Report & Test Blueprint]:")
    print(result["assistant_report"])


if __name__ == "__main__":
    main()
