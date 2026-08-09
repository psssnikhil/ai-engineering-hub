"""
Project 10: E-Commerce AI Shopping Copilot & Long-Term Memory
================================================================
Domain: E-Commerce & Retail Customer Support

Features:
  1. Semantic User Memory Store: Simulates semantic profile matching to inject preference context.
  2. SQL-Like Parameterized Catalog Search: Query builder simulating safe parameter execution.
  3. Personalized Scoring Boost: Dynamically ranks catalog items using profile correlation.
  4. Multi-turn checkout suggestion loop.
"""

import os
import sys
import json
import math
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from labs.common.gateway import LLMGateway

# Rich Mock Product Catalog
PRODUCT_INVENTORY = [
    {"sku": "SKU-PRO-16", "title": "UltraBook Pro 16-inch", "category": "Laptops", "price": 1899.00, "in_stock": True, "tags": ["lightweight", "developer", "high-performance"]},
    {"sku": "SKU-AIR-13", "title": "UltraBook Light 13-inch", "category": "Laptops", "price": 1099.00, "in_stock": True, "tags": ["lightweight", "student", "portable"]},
    {"sku": "SKU-GAM-17", "title": "Apex Gaming Laptop 17-inch", "category": "Laptops", "price": 2199.00, "in_stock": True, "tags": ["gaming", "heavy", "high-performance"]},
    {"sku": "SKU-ANC-HEAD", "title": "Wireless ANC Headphones", "category": "Audio", "price": 299.00, "in_stock": True, "tags": ["noise-canceling", "travel", "audio"]},
    {"sku": "SKU-EAR-BUD", "title": "Mini True Wireless Earbuds", "category": "Audio", "price": 129.00, "in_stock": False, "tags": ["waterproof", "sport"]},
]


# --- Secure Parameterized Inventory Finder ---

def search_product_inventory(
    category: str,
    max_price: Optional[float] = None,
    must_have_tags: Optional[List[str]] = None,
    only_in_stock: bool = True
) -> str:
    """Safe, parameterized catalog search simulating prepared SQL statement inputs."""
    # Ensure parameter types are validated
    if not isinstance(category, str):
        return "Error: Category parameter must be a string."
    if max_price is not None and not isinstance(max_price, (int, float)):
        return "Error: Max price must be a numeric value."

    results = []
    for p in PRODUCT_INVENTORY:
        # Category filter
        if category.lower() != p["category"].lower():
            continue
            
        # Price constraint
        if max_price is not None and p["price"] > max_price:
            continue
            
        # Stock constraint
        if only_in_stock and not p["in_stock"]:
            continue
            
        # Tag filtering
        if must_have_tags:
            match = True
            for tag in must_have_tags:
                if tag.lower() not in [t.lower() for t in p["tags"]]:
                    match = False
                    break
            if not match:
                continue
                
        results.append(p)
        
    return json.dumps(results)


TOOLS_ECOMMERCE = [
    {
        "type": "function",
        "function": {
            "name": "search_product_inventory",
            "description": "Query product catalog with safe parameter filters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "e.g. Laptops, Audio"},
                    "max_price": {"type": "number", "description": "Strict maximum budget constraint"},
                    "must_have_tags": {
                        "type": "array", 
                        "items": {"type": "string"},
                        "description": "List of feature tags (e.g. ['gaming', 'lightweight'])"
                    },
                    "only_in_stock": {"type": "boolean", "description": "Filter out out-of-stock items"}
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
    preferred_category: str
    max_budget: float
    interests: List[str] = field(default_factory=list)
    previous_purchases: List[str] = field(default_factory=list)


class ECommerceShoppingCopilot:
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()

    def rank_products_with_memory(self, products: List[Dict[str, Any]], profile: UserMemoryProfile) -> List[Tuple[Dict[str, Any], float]]:
        """Calculates interest-correlation scores (personalization boost) to rank items."""
        scored = []
        for p in products:
            base_score = 1.0
            
            # Align category match
            if p["category"].lower() == profile.preferred_category.lower():
                base_score += 0.5
                
            # Align interests/tags overlaps
            overlap_interests = set(profile.interests).intersection(set(p["tags"]))
            base_score += len(overlap_interests) * 0.4
            
            # Check budget alignment: penalize products exceeding budget
            if p["price"] > profile.max_budget:
                base_score -= 1.0

            scored.append((p, round(base_score, 2)))
            
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored

    def assist_user(self, user_profile: UserMemoryProfile, user_query: str) -> Dict[str, Any]:
        # Formulate memory summary text to inject into systemic context
        memory_str = (
            f"User Profile Memory context ({user_profile.user_id}):\n"
            f"- Preferred Category: {user_profile.preferred_category}\n"
            f"- Budget Cap: ${user_profile.max_budget}\n"
            f"- Verified Interests: {user_profile.interests}\n"
            f"- Historical Purchases: {user_profile.previous_purchases}"
        )

        system_instruction = (
            "You are a personalized E-Commerce AI Shopping Copilot. Call search_product_inventory "
            "to find products. Recommend the best matching laptop or audio, explaining why they "
            "fit the customer's historical profile and interests."
        )

        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"{memory_str}\n\nCustomer Request: {user_query}"}
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
                    if func:
                        obs = func(**fn_args)
                    else:
                        obs = f"Error: Tool {fn_name} not found."
                        
                    trace.append({"step": step + 1, "tool": fn_name, "args": fn_args, "observation": obs})

                    # Perform personalization ranking boost on raw results if search succeeded
                    if fn_name == "search_product_inventory" and not obs.startswith("Error"):
                        try:
                            items = json.loads(obs)
                            if isinstance(items, list):
                                ranked_pairs = self.rank_products_with_memory(items, user_profile)
                                obs = json.dumps([{"product": p, "personalization_score": s} for p, s in ranked_pairs])
                        except Exception as e:
                            print(f"      [Memory Ranking Exception] {e}")

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

        return {"user_id": user_profile.user_id, "recommendation": "Completed search loop.", "trace": trace}


def main():
    print("=" * 70)
    print("  E-Commerce Personalization Shopping Copilot (Project 10)")
    print("=" * 70 + "\n")

    copilot = ECommerceShoppingCopilot()
    
    # Customer memory file setup
    customer_profile = UserMemoryProfile(
        user_id="usr_developer_99",
        preferred_category="Laptops",
        max_budget=2000.0,
        interests=["lightweight", "developer", "high-performance"],
        previous_purchases=["Wireless ANC Headphones"]
    )

    query = "Suggest a laptop for coding, matching my budget limit and profile."
    print(f"Customer Query: '{query}'")
    print(f"Loading Long-Term memory profile for: {customer_profile.user_id}...\n")

    res = copilot.assist_user(customer_profile, query)
    print(f"Copilot Recommendation Output (via {res.get('provider')}):\n")
    print(res.get("recommendation"))


if __name__ == "__main__":
    main()
