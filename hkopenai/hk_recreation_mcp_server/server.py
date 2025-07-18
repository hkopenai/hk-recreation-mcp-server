"""
Module for creating and running the HK OpenAI Recreation MCP Server.
This module provides functionality to configure and start the server with tools
for accessing data related to creative goods trade in Hong Kong.
"""

from fastmcp import FastMCP

from .tools import creative_goods_trade


def server():
    """
    Create and configure the MCP server.

    Returns:
        FastMCP: Configured MCP server instance with tools for creative goods trade data.
    """
    mcp = FastMCP(name="HK OpenAI recreation Server")

    creative_goods_trade.register(mcp)

    return mcp
