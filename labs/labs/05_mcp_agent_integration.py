"""
Lab 05: Model Context Protocol (MCP) Agent Integration from Scratch
======================================================================
Course 18 & Track: Agent Engineering — MCP Tools & Runtime

Pure Python reference implementation of Model Context Protocol (MCP) concepts:
1. MCP Protocol Message Schema (JSON-RPC 2.0 based)
2. In-memory MCP Server exposing tools (Server Capabilities)
3. MCP Client Handler for tool discovery and execution
4. Autonomous Agent Loop communicating over MCP standard interface

Requirements:
  pip install openai anthropic
  export OPENAI_API_KEY="sk-..."
"""

import json
import uuid
from typing import Dict, Any, List, Optional
from labs.common.gateway import LLMGateway, OpenAIProvider


# ── Step 1: In-Memory MCP Server Specification ────────────────────────────────

class MCPServer:
    """Simulates an MCP Server implementing tools list and tool invocation endpoints."""
    def __init__(self, name: str = "EnterpriseSystemMCPServer"):
        self.name = name
        self._tools = {
            "fetch_user_profile": {
                "description": "Fetch user profile details by user ID from enterprise directory",
                "parameters": {
                    "type": "object",
                    "properties": {"user_id": {"type": "string"}},
                    "required": ["user_id"]
                },
                "handler": self._fetch_user_profile
            },
            "calculate_tier_discount": {
                "description": "Calculate enterprise pricing discount for given customer tier and annual contract value",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "tier": {"type": "string", "enum": ["silver", "gold", "platinum"]},
                        "acv": {"type": "number"}
                    },
                    "required": ["tier", "acv"]
                },
                "handler": self._calculate_tier_discount
            }
        }

    def handle_json_rpc(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming JSON-RPC 2.0 protocol requests from MCP Client."""
        req_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        if method == "tools/list":
            tools_list = []
            for name, details in self._tools.items():
                tools_list.append({
                    "name": name,
                    "description": details["description"],
                    "inputSchema": details["parameters"]
                })
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"tools": tools_list}
            }

        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            if tool_name not in self._tools:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"}
                }

            handler = self._tools[tool_name]["handler"]
            try:
                result_content = handler(**arguments)
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {"type": "text", "text": json.dumps(result_content)}
                        ]
                    }
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)}
                }

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method '{method}' unsupported"}
        }

    def _fetch_user_profile(self, user_id: str) -> Dict[str, Any]:
        profiles = {
            "usr_9912": {"name": "Alice Chen", "role": "VP Engineering", "tier": "platinum", "acv": 150000.0},
            "usr_4410": {"name": "Bob Smith", "role": "DevOps Lead", "tier": "gold", "acv": 45000.0}
        }
        return profiles.get(user_id, {"error": "User not found", "user_id": user_id})

    def _calculate_tier_discount(self, tier: str, acv: float) -> Dict[str, Any]:
        discounts = {"silver": 0.05, "gold": 0.12, "platinum": 0.25}
        rate = discounts.get(tier.lower(), 0.0)
        discount_amount = acv * rate
        net_price = acv - discount_amount
        return {
            "tier": tier,
            "original_acv": acv,
            "discount_rate_pct": f"{rate * 100}%",
            "discount_amount": discount_amount,
            "net_price": net_price
        }


# ── Step 2: MCP Client Protocol Agent ──────────────────────────────────────────

class MCPAgentClient:
    """Client agent that discovers MCP server capabilities and executes tools via JSON-RPC protocol."""
    def __init__(self, mcp_server: MCPServer, gateway: Optional[LLMGateway] = None):
        self.mcp_server = mcp_server
        self.gateway = gateway or LLMGateway([OpenAIProvider()])
        self.discovered_tools: List[Dict[str, Any]] = []

    def initialize_mcp_connection(self) -> None:
        """Discover tools exposed by the MCP Server via JSON-RPC tools/list."""
        req = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": "tools/list",
            "params": {}
        }
        res = self.mcp_server.handle_json_rpc(req)
        raw_tools = res.get("result", {}).get("tools", [])

        # Convert MCP tool schemas into OpenAI / LLMGateway standard tool schemas
        self.discovered_tools = []
        for t in raw_tools:
            self.discovered_tools.append({
                "type": "function",
                "function": {
                    "name": t["name"],
                    "description": t["description"],
                    "parameters": t["inputSchema"]
                }
            })
        print(f"[MCP Client] Initialized connection to '{self.mcp_server.name}'. Discovered {len(self.discovered_tools)} tools.")

    def run(self, prompt: str, max_steps: int = 5) -> str:
        if not self.discovered_tools:
            self.initialize_mcp_connection()

        messages = [
            {"role": "system", "content": "You are an AI Agent with access to tools over the Model Context Protocol (MCP). Use MCP tools to solve user queries precisely."},
            {"role": "user", "content": prompt}
        ]

        for step in range(max_steps):
            print(f"\n--- MCP Agent Step {step + 1} ---")
            resp = self.gateway.generate(messages=messages, tools=self.discovered_tools, temperature=0.0)

            if resp.tool_calls:
                messages.append({
                    "role": "assistant",
                    "content": resp.content or "",
                    "tool_calls": resp.raw_response.choices[0].message.tool_calls
                })

                for tc in resp.tool_calls:
                    fn_name = tc["name"]
                    fn_args = json.loads(tc["arguments"])
                    print(f"  [MCP Dispatch] Requesting method 'tools/call' for '{fn_name}' with args {fn_args}")

                    # Format JSON-RPC request over MCP
                    mcp_req = {
                        "jsonrpc": "2.0",
                        "id": tc["id"],
                        "method": "tools/call",
                        "params": {
                            "name": fn_name,
                            "arguments": fn_args
                        }
                    }
                    mcp_res = self.mcp_server.handle_json_rpc(mcp_req)

                    # Extract result content
                    if "result" in mcp_res:
                        obs = mcp_res["result"]["content"][0]["text"]
                    else:
                        obs = json.dumps(mcp_res.get("error", {"message": "MCP Execution Error"}))

                    print(f"  [MCP Response] Received observation: {obs}")

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc["id"],
                        "content": obs
                    })
            else:
                print("  [MCP Agent] Final answer received from model.")
                return resp.content

        return "MCP Agent loop stopped: Max steps reached."


if __name__ == "__main__":
    print("=== Lab 05: Model Context Protocol (MCP) Agent Integration ===")
    server = MCPServer()
    client = MCPAgentClient(server)

    user_prompt = "Lookup profile for user 'usr_9912' and compute their net contract price after tier discount."
    print(f"User Request: {user_prompt}")

    final_result = client.run(user_prompt)
    print(f"\nFinal Result:\n{final_result}")
