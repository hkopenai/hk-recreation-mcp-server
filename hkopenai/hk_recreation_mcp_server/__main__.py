"""Main entry point for the HK Recreation MCP Server."""
from hkopenai_common.cli_utils import cli_main
from . import server

if __name__ == "__main__":
    cli_main(server.main, "HK Recreation MCP Server")
