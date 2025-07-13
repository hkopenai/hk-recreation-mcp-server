"""
Module for creating and running the HK OpenAI Recreation MCP Server.
This module provides functionality to configure and start the server with tools
for accessing data related to creative goods trade in Hong Kong.
"""

from fastmcp import FastMCP
from hkopenai.hk_recreation_mcp_server import tool_creative_goods_trade
from typing import Dict, List, Annotated, Optional
from pydantic import Field


def create_mcp_server():
    """
    Create and configure the MCP server.
    
    Returns:
        FastMCP: Configured MCP server instance with tools for creative goods trade data.
    """
    mcp = FastMCP(name="HK OpenAI recreation Server")

    @mcp.tool(
        description="Domestic Exports, Re-exports and Imports of Creative Goods in Hong Kong"
    )
    def get_creative_goods_trade(
        start_year: Annotated[
            Optional[int], Field(description="Start year of range")
        ] = None,
        end_year: Annotated[
            Optional[int], Field(description="End year of range")
        ] = None,
    ) -> List[Dict]:
        return tool_creative_goods_trade.get_creative_goods_trade(start_year, end_year)

    return mcp


def main(host: str, port: int, sse: bool):
    """
    Main function to run the MCP Server.
    Parses command line arguments and starts the server in either SSE or stdio mode.
    """
    server = create_mcp_server()

    if sse:
        server.run(transport="streamable-http", host=host, port=port)
        print(f"MCP Server running in SSE mode on port {args.port}, bound to {args.host}")
    else:
        server.run()
        print("MCP Server running in stdio mode")


if __name__ == "__main__":
    main()
