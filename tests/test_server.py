"""
Module for testing the MCP server creation and tool registration.
This module contains unit tests to verify the correct setup and behavior of the server.
"""

import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_recreation_mcp_server.server import create_mcp_server


class TestApp(unittest.TestCase):
    """
    Test class for verifying MCP server creation and tool functionality.
    This class tests the initialization of the server and the registration of tools.
    """
    @patch("hkopenai.hk_recreation_mcp_server.server.FastMCP")
    @patch("hkopenai.hk_recreation_mcp_server.server.tool_creative_goods_trade")
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
        server = create_mcp_server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        self.assertEqual(server, mock_server)

        # Verify that the tool decorator was called for each tool function
        self.assertEqual(mock_server.tool.call_count, 1)

        # Get all decorated functions
        decorated_funcs = {
            call.args[0].__name__: call.args[0]
            for call in mock_server.tool.return_value.call_args_list
        }
        self.assertEqual(len(decorated_funcs), 1)

        # Call each decorated function and verify that the correct underlying function is called

        decorated_funcs["get_creative_goods_trade"](start_year=2020, end_year=2021)
        mock_tool_creative_goods_trade.get_creative_goods_trade.assert_called_once_with(
            2020, 2021
        )


if __name__ == "__main__":
    unittest.main()
