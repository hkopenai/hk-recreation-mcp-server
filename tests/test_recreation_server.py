"""
Module for testing the MCP server creation and tool registration.
This module contains unit tests to verify the correct setup and behavior of the server.
"""

import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_recreation_mcp_server.server import server


class TestApp(unittest.TestCase):
    """
    Test class for verifying MCP server creation and tool functionality.
    This class tests the initialization of the server and the registration of tools.
    """

    @patch("hkopenai.hk_recreation_mcp_server.server.FastMCP")
    @patch("hkopenai.hk_recreation_mcp_server.tools.creative_goods_trade")
    def test_create_mcp_server(self, mock_tool_creative_goods_trade, mock_fastmcp):
        """
        Test the creation of the MCP server and the registration of tools.
        Verifies that the server is created correctly and tools are registered as expected.

        Args:
            mock_tool_creative_goods_trade: Mock for the creative goods trade tool module.
            mock_fastmcp: Mock for the FastMCP class.
        """
        # Setup mocks
        mock_server = Mock()

        # Configure mock_server.tool to return a mock that acts as the decorator
        # This mock will then be called with the function to be decorated
        mock_server.tool.return_value = Mock()
        mock_fastmcp.return_value = mock_server

        # Test server creation
        mcp_server_instance = server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        self.assertEqual(mcp_server_instance, mock_server)

        mock_tool_creative_goods_trade.register.assert_called_once_with(mcp_server_instance)


if __name__ == "__main__":
    unittest.main()
