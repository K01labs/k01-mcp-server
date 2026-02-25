"""
Basic usage of the K01 MCP server via direct HTTP.

This example shows how to interact with the MCP server using
standard HTTP requests, without an MCP client. Useful for
scripting and integration testing.

Requires: pip install httpx
"""

import httpx
import json

MCP_URL = "https://mcp.k01.is/mcp"
API_KEY = "YOUR_API_KEY"  # Replace with your actual key

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


def mcp_request(method: str, params: dict | None = None, request_id: int = 1) -> dict:
    """Send a JSON-RPC request to the MCP server."""
    payload = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
    }
    if params:
        payload["params"] = params

    response = httpx.post(MCP_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()


def main():
    # 1. Initialize the MCP session
    init = mcp_request("initialize")
    server_info = init["result"]["serverInfo"]
    print(f"Connected to: {server_info['name']} v{server_info['version']}")

    # 2. List available tools
    tools = mcp_request("tools/list", request_id=2)
    print(f"\nAvailable tools: {len(tools['result']['tools'])}")
    for tool in tools["result"]["tools"]:
        print(f"  - {tool['name']}: {tool['description'][:60]}...")

    # 3. Generate a small cohort
    result = mcp_request(
        "tools/call",
        params={
            "name": "generate_synthetic_cohort",
            "arguments": {
                "count": 5,
                "condition": "E11.9",
                "age_min": 40,
                "age_max": 65,
                "seed": 42,
            },
        },
        request_id=3,
    )

    content = result["result"]["content"][0]["text"]
    print(f"\nGenerated cohort:\n{content[:500]}...")


if __name__ == "__main__":
    main()
