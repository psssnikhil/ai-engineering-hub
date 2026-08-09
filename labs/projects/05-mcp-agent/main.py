"""
Project 05: Model Context Protocol (MCP) Agent Integration from Scratch
======================================================================
Course 18 & Track: Agent Engineering — MCP Tools & Runtime

Features:
  1. JSON-RPC 2.0 Compliant Layer: Standard JSON-RPC framing and status definitions.
  2. Complete MCP Lifecycle: Handles initialize handshake, tools list, tools call, and resource reading.
  3. Dynamic Resource Server: Exposes mock local configuration and documentation resources.
  4. Robust Error Mapping: Standard JSON-RPC error codes (-32601 Method Not Found, -32602 Invalid Params, etc.)
  5. Multi-provider LLM gateway reasoning loop using client-side tool mappings.
"""

import os
import sys
import json
import uuid
from typing import Dict, Any, List, Optional, Tuple

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from labs.common.gateway import LLMGateway


# --- JSON-RPC 2.0 Error Codes ---
PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603


class MCPServer:
    """Simulates a fully-compliant Model Context Protocol Server with dynamic resources and tools."""
    def __init__(self, name: str = "EnterpriseSystemMCPServer", version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.initialized = False
        
        # Tools definitions
        self._tools = {
            "fetch_user_profile": {
                "description": "Fetch user profile details by user ID from enterprise directory",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "Unified User Identifier"}
                    },
                    "required": ["user_id"]
                },
                "handler": self._fetch_user_profile
            },
            "calculate_tier_discount": {
                "description": "Calculate enterprise pricing discount for given customer tier and annual contract value",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "tier": {"type": "string", "enum": ["silver", "gold", "platinum"], "description": "Customer pricing tier"},
                        "acv": {"type": "number", "description": "Annual Contract Value"}
                    },
                    "required": ["tier", "acv"]
                },
                "handler": self._calculate_tier_discount
            }
        }

        # Resources definitions
        self._resources = {
            "mcp://docs/sla_policy.md": {
                "name": "Service Level Agreement (SLA) Policy",
                "mimeType": "text/markdown",
                "content": "# Enterprise SLA Policy\n- Platinum SLA: 99.99% Availability & 2hr Response Time.\n- Gold SLA: 99.9% Availability & 4hr Response Time."
            },
            "mcp://config/system_manifest.json": {
                "name": "System Configuration Manifest",
                "mimeType": "application/json",
                "content": json.dumps({"environment": "production", "active_regions": ["us-east-1", "eu-central-1"]})
            }
        }

    def handle_request(self, request_json: str) -> str:
        """Central entrypoint handling raw string communications mimicking a stdio/network pipe."""
        try:
            request = json.loads(request_json)
        except json.JSONDecodeError:
            return json.dumps(self._make_error_response(None, PARSE_ERROR, "Parse error: Invalid JSON string."))

        req_id = request.get("id")
        
        # Verify JSON-RPC version
        if request.get("jsonrpc") != "2.0":
            return json.dumps(self._make_error_response(req_id, INVALID_REQUEST, "Invalid request: Must specify JSON-RPC 2.0 version."))

        method = request.get("method")
        params = request.get("params", {})

        # 1. Initialization Phase Handshake
        if method == "initialize":
            self.initialized = True
            result = {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                    "resources": {}
                },
                "serverInfo": {
                    "name": self.name,
                    "version": self.version
                }
            }
            return json.dumps(self._make_result_response(req_id, result))

        if not self.initialized:
            return json.dumps(self._make_error_response(req_id, INTERNAL_ERROR, "Server not initialized. Call 'initialize' first."))

        # 2. Tools Capabilities Endpoint
        if method == "tools/list":
            tools_list = []
            for name, details in self._tools.items():
                tools_list.append({
                    "name": name,
                    "description": details["description"],
                    "inputSchema": details["parameters"]
                })
            return json.dumps(self._make_result_response(req_id, {"tools": tools_list}))

        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name not in self._tools:
                return json.dumps(self._make_error_response(req_id, METHOD_NOT_FOUND, f"Method not found: Tool '{tool_name}' unsupported."))

            handler = self._tools[tool_name]["handler"]
            required_args = self._tools[tool_name]["parameters"].get("required", [])
            
            # Param validation check
            for arg in required_args:
                if arg not in arguments:
                    return json.dumps(self._make_error_response(req_id, INVALID_PARAMS, f"Invalid params: Missing required field '{arg}'."))

            try:
                res_payload = handler(**arguments)
                result = {
                    "content": [
                        {"type": "text", "text": json.dumps(res_payload)}
                    ]
                }
                return json.dumps(self._make_result_response(req_id, result))
            except Exception as e:
                return json.dumps(self._make_error_response(req_id, INTERNAL_ERROR, f"Internal tool execution error: {e}"))

        # 3. Resources Capabilities Endpoint
        elif method == "resources/list":
            resources_list = []
            for uri, details in self._resources.items():
                resources_list.append({
                    "uri": uri,
                    "name": details["name"],
                    "mimeType": details["mimeType"]
                })
            return json.dumps(self._make_result_response(req_id, {"resources": resources_list}))

        elif method == "resources/read":
            uri = params.get("uri")
            if uri not in self._resources:
                return json.dumps(self._make_error_response(req_id, INVALID_PARAMS, f"Invalid params: Resource URI '{uri}' not found."))
            
            details = self._resources[uri]
            result = {
                "contents": [
                    {
                        "uri": uri,
                        "mimeType": details["mimeType"],
                        "text": details["content"]
                    }
                ]
            }
            return json.dumps(self._make_result_response(req_id, result))

        # Unsupported method
        return json.dumps(self._make_error_response(req_id, METHOD_NOT_FOUND, f"Method not found: '{method}' is unsupported."))

    def _make_result_response(self, req_id: Any, result: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": result
        }

    def _make_error_response(self, req_id: Any, code: int, message: str) -> Dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": code,
                "message": message
            }
        }

    # Inner tool handlers
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


class MCPAgentClient:
    """Client agent that discovers MCP server capabilities, maps tools, and queries resources."""
    def __init__(self, mcp_server: MCPServer, gateway: Optional[LLMGateway] = None):
        self.mcp_server = mcp_server
        self.gateway = gateway or LLMGateway()
        self.discovered_tools: List[Dict[str, Any]] = []
        self.discovered_resources: List[Dict[str, Any]] = []

    def perform_handshake(self) -> None:
        # Phase 1: Initialize
        init_req = {
            "jsonrpc": "2.0",
            "id": "handshake-1",
            "method": "initialize",
            "params": {
                "clientInfo": {"name": "MCP-Agent-Client", "version": "1.0.0"}
            }
        }
        resp_str = self.mcp_server.handle_request(json.dumps(init_req))
        resp = json.loads(resp_str)
        server_info = resp.get("result", {}).get("serverInfo", {})
        print(f"[MCP Handshake] Connected to Server: {server_info.get('name')} v{server_info.get('version')}")

        # Phase 2: Get tools list
        tools_req = {"jsonrpc": "2.0", "id": "handshake-2", "method": "tools/list"}
        resp_str = self.mcp_server.handle_request(json.dumps(tools_req))
        resp = json.loads(resp_str)
        raw_tools = resp.get("result", {}).get("tools", [])

        # Adapt MCP tool schemas to standard LLM format
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

        # Phase 3: Get resources list
        res_req = {"jsonrpc": "2.0", "id": "handshake-3", "method": "resources/list"}
        resp_str = self.mcp_server.handle_request(json.dumps(res_req))
        resp = json.loads(resp_str)
        self.discovered_resources = resp.get("result", {}).get("resources", [])

        print(f"[MCP Handshake] Setup complete. Active Tools: {len(self.discovered_tools)} | Active Resources: {len(self.discovered_resources)}")

    def read_resource(self, uri: str) -> str:
        req = {
            "jsonrpc": "2.0",
            "id": f"res-read-{uuid.uuid4().hex[:6]}",
            "method": "resources/read",
            "params": {"uri": uri}
        }
        resp_str = self.mcp_server.handle_request(json.dumps(req))
        resp = json.loads(resp_str)
        if "error" in resp:
            return f"Error reading resource: {resp['error'].get('message')}"
        return resp["result"]["contents"][0]["text"]

    def run(self, user_prompt: str, max_steps: int = 5) -> str:
        # Perform handshake if not done
        if not self.discovered_tools:
            self.perform_handshake()

        # Add resources definitions directly into the agent system context
        resources_ctx = "\n".join(f"- URI: {r['uri']} ({r['name']})" for r in self.discovered_resources)
        
        system_content = (
            "You are an autonomous AI Agent communicating over Model Context Protocol (MCP).\n"
            "You have access to tools and resources. To read a resource (e.g. SLA documents or configs), "
            "mention its URI in your final report or consult it if you have a tool. Since you don't have a direct "
            "read_resource tool in the schemas, request information or format it using existing tools.\n"
            f"Available Resources on MCP Server:\n{resources_ctx}"
        )

        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_prompt}
        ]

        for step in range(max_steps):
            print(f"\n--- MCP Agent Step {step + 1} ---")
            resp = self.gateway.generate(messages=messages, tools=self.discovered_tools, temperature=0.0)

            if resp.tool_calls:
                messages.append({
                    "role": "assistant",
                    "content": resp.content or "",
                    "tool_calls": resp.raw_response.choices[0].message.tool_calls if resp.raw_response else None
                })

                for tc in resp.tool_calls:
                    fn_name = tc["name"]
                    fn_args = json.loads(tc["arguments"]) if isinstance(tc["arguments"], str) else tc["arguments"]
                    
                    print(f"  [Client dispatch -> JSON-RPC] Requesting '{fn_name}' with arguments: {fn_args}")

                    # Form MCP JSON-RPC call
                    mcp_req = {
                        "jsonrpc": "2.0",
                        "id": tc["id"],
                        "method": "tools/call",
                        "params": {
                            "name": fn_name,
                            "arguments": fn_args
                        }
                    }
                    
                    # Execute on MCP server
                    server_resp_str = self.mcp_server.handle_request(json.dumps(mcp_req))
                    server_resp = json.loads(server_resp_str)

                    # Extract result or error
                    if "result" in server_resp:
                        obs = server_resp["result"]["content"][0]["text"]
                    else:
                        obs = f"Error: {server_resp.get('error', {}).get('message', 'MCP execute error')}"

                    print(f"  [Server response -> JSON-RPC] Observation: {obs}")

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc["id"],
                        "content": obs
                    })
            else:
                return resp.content

        return "Agent stopped: Max steps reached."


if __name__ == "__main__":
    print("=== Running MCP Agent Integration System ===")
    server = MCPServer()
    client = MCPAgentClient(server)
    
    # 1. Run direct resource read first to verify capabilities
    print("\n--- Verifying Direct MCP Resource Fetching ---")
    sla_content = client.read_resource("mcp://docs/sla_policy.md")
    print(f"Resource Content (mcp://docs/sla_policy.md):\n{sla_content}\n")

    # 2. Run agent reasoning loop
    goal = "Query user profile usr_9912, calculate discount for their tier and contract value, and summarize the result."
    print("--- Running Agent Loop ---")
    answer = client.run(goal)
    print(f"\nFinal Answer:\n{answer}")
