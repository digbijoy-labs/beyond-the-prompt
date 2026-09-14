"""
Part 4 Demonstration: Model Context Protocol (MCP) JSON-RPC 2.0 Host
"""

from core.protocols.mcp_server import MCPServer, MCPRequest


def main():
    print("=== Beyond the Prompt: Part 4 MCP Server Demonstration ===")
    server = MCPServer(server_name="production-mcp-gateway")

    # Register tool conforming to MCP 2026-07-28
    def calculate_risk(portfolio_val: float, beta: float) -> float:
        return portfolio_val * beta * 0.05

    server.register_tool(
        name="calculate_risk",
        description="Calculates portfolio downside risk coefficient",
        input_schema={
            "type": "object",
            "properties": {
                "portfolio_val": {"type": "number"},
                "beta": {"type": "number"},
            },
            "required": ["portfolio_val", "beta"],
        },
        handler=calculate_risk,
    )

    # 1. Discover Tools via MCP Protocol
    list_req = MCPRequest(id="req-1", method="tools/list")
    list_res = server.handle_request(list_req)
    print(f"\nDiscovered MCP Tools: {list_res.result}")

    # 2. Invoke Tool via MCP Protocol
    call_req = MCPRequest(
        id="req-2",
        method="tools/call",
        params={
            "name": "calculate_risk",
            "arguments": {"portfolio_val": 12400000.0, "beta": 1.45},
        },
    )
    call_res = server.handle_request(call_req)
    print(f"\nMCP Tool Call Result: {call_res.result}")
    print("\n=== Demonstration Complete ===")


if __name__ == "__main__":
    main()
