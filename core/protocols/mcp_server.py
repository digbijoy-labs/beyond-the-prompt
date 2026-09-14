"""
Model Context Protocol (MCP) Server Reference Blueprint (Chapter 14)
Implements JSON-RPC 2.0 tool and resource registration conforming to MCP 2026-07-28.
"""

from __future__ import annotations

from typing import Any, Callable
from pydantic import BaseModel, Field


class MCPTool(BaseModel):
    name: str
    description: str
    input_schema: dict[str, Any]


class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: str | int
    method: str
    params: dict[str, Any] = Field(default_factory=dict)


class MCPResponse(BaseModel):
    jsonrpc: str = "2.0"
    id: str | int
    result: Any = None
    error: dict[str, Any] | None = None


class MCPServer:
    """
    Lightweight, production-grade Model Context Protocol (MCP) host server.
    Exposes tool discovery (tools/list) and tool actuation (tools/call).
    """

    def __init__(self, server_name: str = "beyond-the-prompt-mcp"):
        self.server_name = server_name
        self.tools: dict[str, tuple[MCPTool, Callable]] = {}

    def register_tool(self, name: str, description: str, input_schema: dict[str, Any], handler: Callable) -> None:
        self.tools[name] = (MCPTool(name=name, description=description, input_schema=input_schema), handler)

    def handle_request(self, req: MCPRequest) -> MCPResponse:
        if req.method == "tools/list":
            return MCPResponse(
                id=req.id,
                result={"tools": [t.model_dump() for t, _ in self.tools.values()]},
            )
        elif req.method == "tools/call":
            tool_name = req.params.get("name")
            arguments = req.params.get("arguments", {})
            if tool_name not in self.tools:
                return MCPResponse(
                    id=req.id,
                    error={"code": -32601, "message": f"Method/Tool '{tool_name}' not found"},
                )
            _, handler = self.tools[tool_name]
            try:
                output = handler(**arguments)
                return MCPResponse(
                    id=req.id,
                    result={"content": [{"type": "text", "text": str(output)}]},
                )
            except Exception as e:
                return MCPResponse(
                    id=req.id,
                    error={"code": -32000, "message": str(e)},
                )
        else:
            return MCPResponse(
                id=req.id,
                error={"code": -32600, "message": f"Unsupported method: {req.method}"},
            )
