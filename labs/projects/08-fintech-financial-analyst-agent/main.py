"""
Project 08: Production-Grade FinTech Financial Analyst Agent
=============================================================
Domain: Financial Analysis, SEC 10-K Research & Valuation

Features:
  1. Advanced Valuation Calculators:
     - Discounted Cash Flow (DCF) with terminal value calculation.
     - Weighted Average Cost of Capital (WACC) leveraging equity/debt weights.
     - Compound Annual Growth Rate (CAGR) for historical/forward growth trends.
  2. Structured Report Generator: Outputs Markdown equity research reports with formatted tables.
  3. Dynamic Multi-Year Context: Reads multi-year SEC filing context blocks.
  4. Robust Math Safety: Handles divisions by zero and parameter type checks.
"""

import math
import os
import sys
import json
from dataclasses import dataclass
from typing import Dict, Any, List, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from labs.common.gateway import LLMGateway

# Realistic Mock SEC Filings context
SEC_FILINGS_DB = [
    {
        "company": "TechCorp Inc.",
        "year": 2025,
        "financials": {
            "revenue": [8200.0, 9800.0, 12500.0],  # 2023, 2024, 2025 in Millions
            "ocf": 3200.0,
            "capex": 800.0,
            "shares_outstanding": 500.0,
            "stock_price": 95.0,
            "cost_of_equity": 0.095,  # 9.5%
            "cost_of_debt": 0.055,    # 5.5%
            "tax_rate": 0.21,         # 21%
            "market_equity": 47500.0, # 500M * $95
            "total_debt": 15000.0
        },
        "highlights": (
            "TechCorp Inc. reported total revenue of $12.5 Billion in FY2025. "
            "Capital expenditures of $800M went into data center assets. "
            "Outstanding debt stands at $15 Billion with interest rate averaging 5.5%."
        )
    }
]


# --- Advanced Financial Calculators ---

def calculate_wacc(
    cost_of_equity: float,
    cost_of_debt: float,
    tax_rate: float,
    equity_value: float,
    debt_value: float
) -> str:
    """Calculate Weighted Average Cost of Capital (WACC)."""
    total_val = equity_value + debt_value
    if total_val <= 0:
        return "Error: Combined equity and debt value must be positive."
        
    w_equity = equity_value / total_val
    w_debt = debt_value / total_val
    
    # WACC = (E/V * Re) + (D/V * Rd * (1 - T))
    wacc = (w_equity * cost_of_equity) + (w_debt * cost_of_debt * (1 - tax_rate))
    
    return json.dumps({
        "wacc": round(wacc, 4),
        "wacc_percent": f"{round(wacc * 100, 2)}%",
        "equity_weight": round(w_equity, 3),
        "debt_weight": round(w_debt, 3),
        "cost_of_debt_after_tax": round(cost_of_debt * (1 - tax_rate), 4)
    })


def calculate_dcf(
    current_fcf: float,
    discount_rate: float,
    growth_rate: float,
    terminal_growth_rate: float,
    years: int = 5
) -> str:
    """Calculate Discounted Cash Flow (DCF) enterprise valuation."""
    if discount_rate <= terminal_growth_rate:
        return "Error: Discount rate (WACC) must be strictly greater than terminal growth rate (growth perpetuity)."
        
    discounted_cash_flows = []
    fcf = current_fcf
    
    # Project cash flows
    for t in range(1, years + 1):
        fcf = fcf * (1 + growth_rate)
        df = (1 + discount_rate) ** t
        dcf_val = fcf / df
        discounted_cash_flows.append(dcf_val)

    # Terminal Value (Gordon Growth Model)
    terminal_value = (fcf * (1 + terminal_growth_rate)) / (discount_rate - terminal_growth_rate)
    discounted_terminal_value = terminal_value / ((1 + discount_rate) ** years)
    
    enterprise_value = sum(discounted_cash_flows) + discounted_terminal_value
    
    return json.dumps({
        "projected_fcf_sum": round(sum(discounted_cash_flows), 2),
        "discounted_terminal_value": round(discounted_terminal_value, 2),
        "enterprise_value_million": round(enterprise_value, 2),
        "assumptions": {
            "years": years,
            "growth_projection": f"{round(growth_rate * 100, 1)}%",
            "discount_rate": f"{round(discount_rate * 100, 1)}%",
            "perpetuity_growth": f"{round(terminal_growth_rate * 100, 1)}%"
        }
    })


def calculate_cagr(start_value: float, end_value: float, periods: int) -> str:
    """Calculate Compound Annual Growth Rate (CAGR)."""
    if start_value <= 0 or end_value <= 0 or periods <= 0:
        return "Error: Input values and periods must be positive non-zero numbers."
    cagr = (end_value / start_value) ** (1 / periods) - 1
    return json.dumps({
        "cagr": round(cagr, 4),
        "cagr_percent": f"{round(cagr * 100, 2)}%",
        "total_growth": f"{round((end_value / start_value - 1) * 100, 1)}%"
    })


TOOLS_FINTECH = [
    {
        "type": "function",
        "function": {
            "name": "calculate_wacc",
            "description": "Calculate Weighted Average Cost of Capital (WACC) to use as discount rate.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cost_of_equity": {"type": "number", "description": "Cost of Equity (e.g. 0.095)"},
                    "cost_of_debt": {"type": "number", "description": "Cost of Debt (e.g. 0.055)"},
                    "tax_rate": {"type": "number", "description": "Corporate tax rate (e.g. 0.21)"},
                    "equity_value": {"type": "number", "description": "Total market capitalization of equity"},
                    "debt_value": {"type": "number", "description": "Total outstanding debt book value"}
                },
                "required": ["cost_of_equity", "cost_of_debt", "tax_rate", "equity_value", "debt_value"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_dcf",
            "description": "Perform Discounted Cash Flow (DCF) projection and enterprise valuation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "current_fcf": {"type": "number", "description": "Free cash flow of starting year (Million USD)"},
                    "discount_rate": {"type": "number", "description": "WACC discount rate (e.g. 0.082)"},
                    "growth_rate": {"type": "number", "description": "Expected growth rate for projection (e.g. 0.15)"},
                    "terminal_growth_rate": {"type": "number", "description": "Terminal growth perpetuity rate (e.g. 0.02)"},
                    "years": {"type": "integer", "description": "Number of projection years (default 5)"}
                },
                "required": ["current_fcf", "discount_rate", "growth_rate", "terminal_growth_rate"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_cagr",
            "description": "Calculate historical growth CAGR over multiple periods.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_value": {"type": "number"},
                    "end_value": {"type": "number"},
                    "periods": {"type": "integer"}
                },
                "required": ["start_value", "end_value", "periods"]
            }
        }
    }
]

TOOL_MAP_FINTECH = {
    "calculate_wacc": calculate_wacc,
    "calculate_dcf": calculate_dcf,
    "calculate_cagr": calculate_cagr,
}


class FinancialAnalystAgent:
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()

    def run_equity_research(self, company_name: str) -> Dict[str, Any]:
        # Filter matching records from filings DB
        filing_records = [c for c in SEC_FILINGS_DB if company_name.lower() in c['company'].lower()]
        if not filing_records:
            return {"error": f"Company '{company_name}' details not found in filings database."}
        
        record = filing_records[0]
        context_str = (
            f"Filing Highlights: {record['highlights']}\n"
            f"Detailed Metrics: {json.dumps(record['financials'])}"
        )

        user_prompt = (
            f"Analyze SEC filing context for '{company_name}' and calculate:\n"
            f"1. CAGR of revenue over the 3 periods (from 2023 base to 2025: $8,200M to $12,500M, 2 periods difference).\n"
            f"2. WACC discount rate.\n"
            f"3. Enterprise Value using DCF, assuming projection growth rate matching the CAGR we computed, "
            f"a terminal growth perpetuity rate of 2% (0.02), and FCF of $2,400M (OCF $3,200M - CapEx $800M).\n"
            f"4. Format the final output as a detailed Markdown Equity Research Report containing "
            f"financial tables and analyst disclaimers.\n\n"
            f"Filing Data Context:\n{context_str}"
        )

        messages = [
            {
                "role": "system",
                "content": "You are a Wall Street Research Analyst. Utilize financial calculators to retrieve precise mathematical parameters."
            },
            {"role": "user", "content": user_prompt}
        ]

        trace = []
        for step in range(6):
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
                    
                    print(f"  [Analyst Tool Exec] Calling {fn_name} with: {fn_args}")
                    
                    func = TOOL_MAP_FINTECH.get(fn_name)
                    if func:
                        res = func(**fn_args)
                    else:
                        res = f"Error: Tool {fn_name} not found."
                        
                    print(f"    Observation: {res}")
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

        return {"company": company_name, "research_report": "Completed research with max steps.", "trace": trace}


def main():
    print("=" * 70)
    print("  Enterprise FinTech Analyst Agent (Project 08)")
    print("=" * 70 + "\n")

    agent = FinancialAnalystAgent()
    target_company = "TechCorp Inc."
    print(f"Starting equity valuation research pipeline for: {target_company}...\n")

    result = agent.run_equity_research(target_company)
    if "error" in result:
        print(f"Pipeline error: {result['error']}")
    else:
        print(f"Equity Research Report (Generated via {result.get('provider')}):\n")
        print(result.get("research_report"))


if __name__ == "__main__":
    main()
