"""
Console-script entry point for hkopenai.hk_recreation_mcp_server.
"""

from hkopenai_common.cli_utils import cli_main
from .server import server


def main():
    """Console-script entry point for the hk recreation mcp server."""
    cli_main(server, "hk recreation mcp server")


if __name__ == "__main__":
    main()
