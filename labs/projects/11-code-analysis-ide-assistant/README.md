# Project 11: Code Analysis & IDE Assistant

A developer coding assistant featuring Python AST parsing, static security vulnerability detection (SQL injection risk), and automated secure refactoring.

```mermaid
flowchart TD
    Source["Python Source Code"] --> AST["AST Parser & Security Scanner"]
    AST --> Vulnerability{"Vulnerability Found?"}
    Vulnerability -- Yes --> Refactor["AI Secure Refactorer"]
    Vulnerability -- No --> Pass["Code Safety Verified"]
    Refactor --> SecureCode["Fixed Python Code"]
```

## Quick Example Code

```python
from main import CodeAnalysisAssistant

assistant = CodeAnalysisAssistant()
vulnerabilities = assistant.scan_code("query = f'SELECT * FROM users WHERE id = {user_id}'")
print("Vulnerabilities Detected:", vulnerabilities)
```

## Quickstart

```bash
python main.py
```
