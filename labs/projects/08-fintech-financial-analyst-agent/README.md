# Project 08: FinTech Financial Analyst Agent

An equity research & SEC filing analysis agent for financial metric extraction, valuation ratio calculation (P/E, FCF, DCF), and structured equity report synthesis.

```mermaid
flowchart LR
    SEC["SEC 10-K Filing Data"] --> Extraction["Financial Metric Extractor"]
    Extraction --> Valuation["Ratio Calculator (P/E, FCF)"]
    Valuation --> Agent["ReAct Financial Agent"]
    Agent --> Memo["Structured Investment Memo"]
```

## Quick Example Code

```python
from main import FinancialAnalystAgent

agent = FinancialAnalystAgent()
report = agent.analyze_ticker("AAPL")
print(report)
```

## Quickstart

```bash
python main.py
```
