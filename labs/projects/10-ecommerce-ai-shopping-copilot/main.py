"""
Project 10: E-Commerce AI Shopping Copilot & Long-Term Memory
================================================================
Domain: E-Commerce & Retail Customer Support

A personalized shopping copilot featuring:
1. Long-Term User Preference & Order History Memory Store
2. SQL Product Inventory Search & Order Status Check Tools
3. Structured JSON Checkout & Recommendation Synthesis

Usage:
  python main.py
"""

import os
import sys
import json
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from labs.common.gateway import LLMGateway


# Mock E-Commerce Database
PRODUCT_INVENTORY = [
    {"sku": "SKU-PRO-MAX", "title": "UltraBook Pro 16-inch", "category": "Laptops", "price": 1899.00, "in_stock": True},
    {"sku": "SKU-AIR-13", "title": "UltraBook Light 13-inch", "category": "Laptops", "price": 1099.00, "in_stock": True},
    {"sku": "SKU-ANC-HEAD", "title": "Wireless ANC Noise Canceling Headphones", "category": "Audio", "price": 299.00, "in_stock": True},
]


def search_product_inventory(category: str, max_price: float = 2000.0) -> str:
    """Search product catalog by category and budget price."""
    matching = [p for p in PRODUCT_INVENTORY if category.lower() in p["category"].lower() and p["price"] <= max_price]
    return json.dumps(matching if matching else {"notice": "No products match criteria"})


TOOLS_ECOMMERCE = [
    {
        "type": "function",
        "function": {
            "name": "search_product_inventory",
            "description": "Search product inventory by product category and budget price limit",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {"type": "string"},
                    "max_price": {"type": "number"}
                },
                "required": ["category"]
            }
        }
    }
]

TOOL_MAP_ECOMMERCE = {
    "search_product_inventory": search_product_inventory
}


@dataclass
class UserMemoryProfile:
    user_id: str
    preferred_category: str = "Laptops"
    max_budget: float = 1500.0
    previous_purchases: List[str] = field(default_factory=lambda: ["Wireless ANC Noise Canceling Headphones"])


class ECommerceShoppingCopilot:
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()

    def assist_user(self, user_profile: UserMemoryProfile, user_query: str) -> Dict[str, Any]:
        memory_str = (
            f"User Profile ({user_profile.user_id}): Preferred Category={user_profile.preferred_category}, "
            f"Budget Limit=${user_profile.max_budget}, Past Purchases={user_profile.previous_purchases}"
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a personalized E-Commerce AI Shopping Copilot. Use inventory tools to find products "
                    "matching the user's budget and long-term memory preferences."
                )
            },
            {"role": "user", "content": f"{memory_str}\n\nUser Request: {user_query}"}
        ]

        trace = []
        for step in range(5):
            resp = self.gateway.generate(messages=messages, tools=TOOLS_ECOMMERCE, temperature=0.0)

            if resp.tool_calls:
                messages.append({
                    "role": "assistant",
                    "content": resp.content or "",
                    "tool_calls": resp.raw_response.choices[0].message.tool_calls if resp.raw_response else None
                })

                for tc in resp.tool_calls:
                    fn_name = tc["name"]
                    fn_args = json.loads(tc["arguments"]) if isinstance(tc["arguments"], str) else tc["arguments"]
                    func = TOOL_MAP_ECOMMERCE.get(fn_name)
                    obs = func(**fn_args) if func else f"Error: Tool {fn_name} not found"
                    trace.append({"step": step + 1, "tool": fn_name, "args": fn_args, "observation": obs})

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc["id"],
                        "content": obs
                    })
            else:
                return {
                    "user_id": user_profile.user_id,
                    "recommendation": resp.content,
                    "provider": resp.provider_name,
                    "trace": trace
                }

        return {"user_id": user_profile.user_id, "recommendation": "Completed assistance.", "trace": trace}


def main():
    print("=" * 60)
    print("  E-Commerce AI Shopping Copilot (Project 10)")
    print("=" * 60 + "\n")

    copilot = ECommerceShoppingCopilot()
    user_mem = UserMemoryProfile(user_id="usr_laptop_buyer_99", preferred_category="Laptops", max_budget=1500.0)

    query = "Recommend a lightweight laptop under my budget limit."
    print(f"User ({user_mem.user_id}) Query: {query}\n")

    res = copilot.assist_user(user_mem, query)
    print(f"Copilot Recommendation (Generated via {res.get('provider')}):\n")
    print(res.get("recommendation"))


if __name__ == "__main__":
    main()
