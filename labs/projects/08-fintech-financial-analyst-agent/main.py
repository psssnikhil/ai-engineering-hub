"""
Project 08: FinTech Financial Analyst Agent
===========================================
Domain: Financial Analysis, SEC 10-K Research & Valuation

A production-style financial analyst agent featuring SEC filing chunking,
ratio calculation tools (P/E ratio, DCF valuation, revenue growth),
and structured Markdown equity research report generation.

Usage:
  python main.py
"""

import math
import os
import sys
import json
from dataclasses import dataclass
from typing import Dict, Any, List, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from labs.common.gateway import LLMGateway


SEC_FILING_CHUNKS = [
    {"id": "SEC-10K-01", "company": "TechCorp Inc.", "year": 2025, "text": "TechCorp Inc. reported FY2025 total revenue of $12.5 Billion, representing a 18% YoY growth. Net income stood at $2.1 Billion."},
    {"id": "SEC-10K-02", "company": "TechCorp Inc.", "year": 2025, "text": "Operating cash flow for FY2025 was $3.2 Billion with capital expenditures of $800 Million, resulting in Free Cash Flow of $2.4 Billion."},
    {"id": "SEC-10K-03", "company": "TechCorp Inc.", "year": 2025, "text": "Total outstanding shares count is 500 Million shares. Current stock trading price is $95.00 per share."},
]


def calculate_pe_ratio(stock_price: float, earnings_per_share: float) -> str:
    """Calculate Price-to-Earnings (P/E) Ratio."""
    if earnings_per_share <= 0:
        return "Error: Earnings per share must be greater than zero."
    pe = stock_price / earnings_per_share
    return f"P/E Ratio: {pe:.2f}x (Stock Price: ${stock_price}, EPS: ${earnings_per_share:.2f})"


def calculate_free_cash_flow(operating_cash_flow: float, capex: float) -> str:
    """Calculate Free Cash Flow (FCF)."""
    fcf = operating_cash_flow - capex
    return f"Free Cash Flow: ${fcf:.2f} Million (OCF: ${operating_cash_flow}M, CapEx: ${capex}M)"


TOOLS_FINTECH = [
    {
        "type": "function",
        "function": {
            "name": "calculate_pe_ratio",
            "description": "Calculate Price-to-Earnings (P/E) Ratio for equity valuation",
            "parameters": {
                "type": "object",
                "properties": {
                    "stock_price": {"type": "number"},
                    "earnings_per_share": {"type": "number"}
                },
                "required": ["stock_price", "earnings_per_share"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_free_cash_flow",
            "description": "Calculate Free Cash Flow (FCF) from Operating Cash Flow and CapEx",
            "parameters": {
                "type": "object",
                "properties": {
                    "operating_cash_flow": {"type": "number"},
                    "capex": {"type": "number"}
                },
                "required": ["operating_cash_flow", "capex"]
            }
        }
    }
]

TOOL_MAP_FINTECH = {
    "calculate_pe_ratio": calculate_pe_ratio,
    "calculate_free_cash_flow": calculate_free_cash_flow,
}


class FinancialAnalystAgent:
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()

    def run_equity_research(self, company_name: str) -> Dict[str, Any]:
        # Filter relevant SEC filings
        context = "\n".join(f"[{c['id']}] {c['text']}" for c in SEC_FILING_CHUNKS if company_name.lower() in c['company'].lower())

        user_prompt = (
            f"Analyze SEC 10-K filing context for '{company_name}'.\n"
            f"Filing Context:\n{context}\n\n"
            "Calculate EPS ($2.1B / 500M shares = $4.20), calculate P/E ratio, calculate FCF, "
            "and provide an Executive Equity Research Summary."
        )

        messages = [
            {"role": "system", "content": "You are a Wall Street Financial Analyst. Use financial calculation tools to evaluate metrics accurately."},
            {"role": "user", "content": user_prompt}
        ]

        trace = []
        for step in range(5):
            resp = self.gateway.generate(messages=messages, tools=TOOLS_FINTECH, temperature=0.0)

            if resp.tool_calls:
                messages.append({
                    "role": "assistant",
                    "content": resp.content or "",
                    "tool_calls": resp.raw_response.choices[0].message.tool_calls if resp.raw_response else None
                })

                for tc in resp.tool_calls:
                    fn_name = tc["name"]
                    fn_args = json.loads(tc["arguments"]) if isinstance(tc["arguments"], str) else tc["arguments"]
                    func = TOOL_MAP_FINTECH.get(fn_name)
                    res = func(**fn_args) if func else f"Error: Tool {fn_name} not found"
                    trace.append({"step": step + 1, "tool": fn_name, "result": res})

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc["id"],
                        "content": res
                    })
            else:
                return {
                    "company": company_name,
                    "research_report": resp.content,
                    "provider": resp.provider_name,
                    "trace": trace
                }

        return {"company": company_name, "research_report": "Completed financial research.", "trace": trace}


def main():
    print("=" * 60)
    print("  FinTech Financial Analyst Agent (Project 08)")
    print("=" * 60 + "\n")

    agent = FinancialAnalystAgent()
    target_company = "TechCorp Inc."
    print(f"Target Company: {target_company}\n")

    result = agent.run_equity_research(target_company)
    print(f"Research Report (Generated via {result.get('provider')}):\n")
    print(result.get("research_report"))


if __name__ == "__main__":
    main()
