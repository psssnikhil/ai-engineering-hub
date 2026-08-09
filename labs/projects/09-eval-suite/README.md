# Project 9: AI Quality Evaluation Suite

An automated AI Quality Evaluation suite that runs offline regressions on golden datasets, scores faithfulness and relevance rubrics, and enforces CI/CD quality gate pass/fail thresholds.

## Features
- **Golden Dataset**: Structured test cases with target prompts, contexts, and keyword requirements.
- **Rubric Scoring**: Automated faithfulness overlap and keyphrase coverage scoring.
- **CI Quality Gate**: Exits with code 0 on success or 1 on failure for GitHub Actions integration.

## Quick Start

```bash
cd labs/projects/09-eval-suite
python main.py
```
