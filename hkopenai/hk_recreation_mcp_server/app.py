import argparse
from fastmcp import FastMCP
from hkopenai.hk_recreation_mcp_server import tool_creative_goods_trade
from typing import Dict, List, Annotated, Optional
from pydantic import Field

def create_mcp_server():
    """Create and configure the MCP server"""
    mcp = FastMCP(name="HK OpenAI recreation Server")

    @mcp.tool(
        description="Domestic Exports, Re-exports and Imports of Creative Goods in Hong Kong"
    )
    def get_creative_goods_trade(
        start_year: Annotated[Optional[int], Field(description="Start year of range")] = None,
        end_year: Annotated[Optional[int], Field(description="End year of range")] = None
    ) -> List[Dict]:
        return tool_creative_goods_trade.get_creative_goods_trade(start_year, end_year)

    return mcp
def main():
    parser = argparse.ArgumentParser(description='HKO MCP Server')
    parser.add_argument('-s', '--sse', action='store_true',
                       help='Run in SSE mode instead of stdio')
    args = parser.parse_args()

    server = create_mcp_server()
    
    if args.sse:
        server.run(transport="streamable-http")
        print("HKO MCP Server running in SSE mode on port 8000")
    else:
        server.run()
        print("HKO MCP Server running in stdio mode")

if __name__ == "__main__":
    main()
