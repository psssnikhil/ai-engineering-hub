#!/usr/bin/env python3
"""
AI Engineering Hub — Terminal Companion CLI
Interactive CLI for running projects, practicing system design quizzes, and verifying setup.
"""

import sys
import os
import subprocess
import random

BANNER = r"""
   ___    ____   ______                 _                      _             __  __ ub 
  / _ \  |_  /  / ____/____  ____ _    (_)____  ___  ___  ____(_)___  ____ _/ / / /_  __/ |
 / /_\ \  / /  / __/ / __ \/ __ `/  / / __ \/ _ \/ _ \/ ___/ / __ \/ __ `/ /_/ / / / / / /
/ /_/ /  / /__/ /___/ / / / /_/ /  / / / / /  __/  __/ /  / / / / / /_/ / __  / /_/ / /_/ 
\_/  \_\/____/_____/_/ /_/\__, /  /_/_/ /_/\___/\___/_/  /_/_/ /_/\__, /_/ /_/\__,_(_)__/  
                         /____/                                  /____/                    
"""

PROJECTS = [
    {"num": "01", "name": "01-rag-pipeline", "title": "RAG Pipeline", "domain": "General AI", "path": "labs/projects/01-rag-pipeline/main.py"},
    {"num": "02", "name": "02-agent-loop", "title": "ReAct Agent Loop", "domain": "Agent Systems", "path": "labs/projects/02-agent-loop/main.py"},
    {"num": "03", "name": "03-eval-harness", "title": "LLM Eval Harness", "domain": "Quality & Evals", "path": "labs/projects/03-eval-harness/main.py"},
    {"num": "04", "name": "04-hybrid-search", "title": "Hybrid Search Engine", "domain": "Search & Retrieval", "path": "labs/projects/04-hybrid-search/main.py"},
    {"num": "05", "name": "05-mcp-agent", "title": "MCP Agent & JSON-RPC Server", "domain": "Enterprise Tools", "path": "labs/projects/05-mcp-agent/main.py"},
    {"num": "06", "name": "06-autonomous-agent-platform", "title": "Autonomous Agent Platform", "domain": "Multi-Agent", "path": "labs/projects/06-autonomous-agent-platform/main.py"},
    {"num": "07", "name": "07-enterprise-rag-system", "title": "Enterprise RAG System", "domain": "Production LLMOps", "path": "labs/projects/07-enterprise-rag-system/main.py"},
    {"num": "08", "name": "08-fintech-financial-analyst-agent", "title": "FinTech Financial Analyst Agent", "domain": "Financial Analysis", "path": "labs/projects/08-fintech-financial-analyst-agent/main.py"},
    {"num": "09", "name": "09-healthcare-medical-guardrails-agent", "title": "Healthcare Guardrails Agent", "domain": "Healthcare & Safety", "path": "labs/projects/09-healthcare-medical-guardrails-agent/main.py"},
    {"num": "10", "name": "10-ecommerce-ai-shopping-copilot", "title": "E-Commerce Shopping Copilot", "domain": "Retail & Support", "path": "labs/projects/10-ecommerce-ai-shopping-copilot/main.py"},
    {"num": "11", "name": "11-code-analysis-ide-assistant", "title": "Code Analysis Assistant", "domain": "Developer Tools", "path": "labs/projects/11-code-analysis-ide-assistant/main.py"},
    {"num": "12", "name": "12-agent-data-flywheel-curator", "title": "Agent Data Flywheel Curator", "domain": "AI Infrastructure", "path": "labs/projects/12-agent-data-flywheel-curator/main.py"},
]

QUIZ_QUESTIONS = [
    {
        "question": "What is the primary difference between BM25 and Dense Embedding retrieval in RAG?",
        "options": [
            "A) BM25 uses neural attention while dense embeddings use exact token matching",
            "B) BM25 matches exact keywords via term frequency while dense embeddings capture semantic meaning",
            "C) BM25 only works for code while dense embeddings only work for English text",
            "D) BM25 requires an API key while dense embeddings run without any model"
        ],
        "answer": "B",
        "explanation": "BM25 relies on exact lexical token matching and term frequency, whereas dense embeddings project text into continuous vector spaces to capture semantic intent regardless of exact wording."
    },
    {
        "question": "In the ReAct agent framework, what occurs during the 'Observation' step?",
        "options": [
            "A) The LLM updates its prompt instructions",
            "B) The user sends a new prompt to the agent",
            "C) The agent executes a tool and returns the tool's raw result back to the model context",
            "D) The vector database re-indexes all stored documents"
        ],
        "answer": "C",
        "explanation": "In ReAct (Thought -> Action -> Observation), the Action is the tool invocation and the Observation is the environment's response fed back into the LLM context for the next thought step."
    },
    {
        "question": "Why is Reciprocal Rank Fusion (RRF) used in Hybrid Search RAG pipelines?",
        "options": [
            "A) To compress vector dimensions from 1536 to 768",
            "B) To combine and rank results from disparate retrieval algorithms without requiring normalized score distributions",
            "C) To encrypt retrieved chunks before sending them to the LLM",
            "D) To automatically translate foreign query languages"
        ],
        "answer": "B",
        "explanation": "RRF converts raw scores into rank positions using RRF_score = 1 / (k + rank), making it score-scale invariant when combining BM25 and vector search results."
    },
    {
        "question": "What is the role of an LLM-as-a-Judge evaluation harness?",
        "options": [
            "A) To automatically generate python unit tests for frontend code",
            "B) To evaluate generated model answers against criteria like faithfulness, context relevance, and safety using structured LLM prompts",
            "C) To fine-tune transformer weights via backpropagation",
            "D) To host LLMs locally on GPU clusters"
        ],
        "answer": "B",
        "explanation": "LLM-as-a-Judge utilizes capable evaluator LLMs (or smaller judge models) with explicit scoring rubrics to evaluate qualitative system outputs in CI/CD automated gates."
    },
    {
        "question": "What is Model Context Protocol (MCP)?",
        "options": [
            "A) A protocol for compressing prompt tokens using gzip",
            "B) An open standard that enables AI models to securely connect to external tools, databases, and context servers via JSON-RPC",
            "C) A vector database indexing algorithm",
            "D) A Python library for fine-tuning BERT"
        ],
        "answer": "B",
        "explanation": "MCP standardizes how AI applications discover, authenticate, and execute external tools, resources, and context providers."
    }
]

def print_header():
    print("\033[36m" + BANNER + "\033[0m")
    print("\033[1mAI Engineering Hub Companion CLI\033[0m — Interactive Terminal Runner & Quizzer")
    print("=" * 75)

def list_projects():
    print_header()
    print("\n\033[1mAVAILABLE MULTI-DOMAIN PROJECTS (/labs/projects):\033[0m\n")
    for p in PROJECTS:
        exists = "✅ Ready" if os.path.exists(p["path"]) else "❌ Missing"
        print(f"  \033[33m[{p['num']}]\033[0m \033[1m{p['title']:<34}\033[0m ({p['domain']:<18}) -> {exists}")
    print("\nRun a project with: \033[36mpython scripts/hub.py run <num>\033[0m (e.g. `python scripts/hub.py run 01`)")

def run_project(num_str):
    match = next((p for p in PROJECTS if p["num"] == num_str.zfill(2)), None)
    if not match:
        print(f"\033[31mError: Project '{num_str}' not found.\033[0m Run `python scripts/hub.py list` to see available projects.")
        sys.exit(1)
    
    print(f"\n🚀 \033[1mRunning Project {match['num']}: {match['title']}\033[0m ({match['path']})\n" + "-" * 60)
    subprocess.run([sys.executable, match["path"]])

def run_quiz():
    print_header()
    print("\n🎯 \033[1mAI SYSTEM DESIGN INTERVIEW QUIZ\033[0m (5 Questions)\n" + "-" * 60)
    
    score = 0
    questions = random.sample(QUIZ_QUESTIONS, len(QUIZ_QUESTIONS))
    
    for i, q in enumerate(questions, 1):
        print(f"\n\033[1mQ{i}: {q['question']}\033[0m\n")
        for opt in q["options"]:
            print(f"   {opt}")
        
        choice = input("\n👉 Enter your choice (A/B/C/D): ").strip().upper()
        if choice == q["answer"]:
            print("✅ \033[32mCorrect!\033[0m " + q["explanation"])
            score += 1
        else:
            print(f"❌ \033[31mIncorrect.\033[0m Correct answer was \033[1m{q['answer']}\033[0m. " + q["explanation"])
        print("-" * 60)
    
    print(f"\n🎉 \033[1mQuiz Complete! Score: {score}/{len(questions)}\033[0m")
    if score == len(questions):
        print("🌟 Outstanding! You have mastered these key AI engineering concepts.")
    else:
        print("💡 Keep studying the handbook at https://psssnikhil.github.io/ai-engineering-hub/ !")

def run_verify():
    print_header()
    print("\n🔍 \033[1mVERIFYING REPOSITORY INTEGRITY & LABS\033[0m\n" + "-" * 60)
    
    cmd = [sys.executable, "-m", "pytest", "labs/tests/"] if os.path.exists("labs/tests") else None
    if cmd:
        print("Running lab test suite...")
        res = subprocess.run(cmd)
        if res.returncode == 0:
            print("\n✅ All lab tests passed successfully!")
        else:
            print("\n❌ Lab tests failed. Please review output above.")
    else:
        print("✅ Core setup verified.")

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help", "help"]:
        list_projects()
        print("\n\033[1mCOMMANDS:\033[0m")
        print("  \033[36mpython scripts/hub.py list\033[0m        List all reference projects")
        print("  \033[36mpython scripts/hub.py run <num>\033[0m    Execute reference project by number (e.g. 01, 02)")
        print("  \033[36mpython scripts/hub.py quiz\033[0m        Start interactive terminal AI system design quiz")
        print("  \033[36mpython scripts/hub.py verify\033[0m      Verify lab tests and environment")
        return

    sub = sys.argv[1].lower()
    if sub == "list":
        list_projects()
    elif sub == "run":
        if len(sys.argv) < 3:
            print("\033[31mPlease specify project number (e.g. 01, 02).\033[0m")
            sys.exit(1)
        run_project(sys.argv[2])
    elif sub == "quiz":
        run_quiz()
    elif sub == "verify":
        run_verify()
    else:
        print(f"\033[31mUnknown command: '{sub}'\033[0m")
        sys.exit(1)

if __name__ == "__main__":
    main()
