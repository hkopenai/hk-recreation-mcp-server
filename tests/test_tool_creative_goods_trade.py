"""
Module for testing the creative goods trade tool functionality.

This module contains unit tests for fetching and processing creative goods trade data.
"""

import unittest
from unittest.mock import patch, MagicMock

from hkopenai.hk_recreation_mcp_server.tools.creative_goods_trade import (
    _get_creative_goods_trade,
    register,
)


class TestCreativeGoodsTrade(unittest.TestCase):
    """
    Test class for verifying creative goods trade functionality.

    This class contains test cases to ensure the data fetching and processing
    for creative goods trade data work as expected.
    """

    def test_get_creative_goods_trade(self):
        """
        Test the retrieval and filtering of creative goods trade data.

        This test verifies that the function correctly fetches and filters data by year range,
        and handles error cases.
        """
        # Mock the CSV data
        mock_csv_data = [
            {
                "Year": "2020",
                "CI_Goods_Cat": "1",
                "Trade_Type": "1",
                "Values": "1000",
                "Percentage": "10.0%",
            },
            {
                "Year": "2020",
                "CI_Goods_Cat": "2",
                "Trade_Type": "2",
                "Values": "2000",
                "Percentage": "20.0%",
            },
            {
                "Year": "2021",
                "CI_Goods_Cat": "1",
                "Trade_Type": "3",
                "Values": "1500",
                "Percentage": "15.0%",
            },
        ]

        with patch(
            "hkopenai.hk_recreation_mcp_server.tools.creative_goods_trade.fetch_csv_from_url"
        ) as mock_fetch_csv_from_url:
            # Setup mock response for successful data fetching
            mock_fetch_csv_from_url.return_value = mock_csv_data

            # Test filtering by year range
            result = _get_creative_goods_trade(start_year=2020, end_year=2020)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["year"], 2020)
            self.assertEqual(result[0]["category"], "Advertising")

            # Test empty result for non-matching years
            result = _get_creative_goods_trade(start_year=2022, end_year=2022)
            self.assertEqual(len(result), 0)

            # Test error handling when fetch_csv_from_url returns an error
            mock_fetch_csv_from_url.return_value = {"error": "CSV fetch failed"}
            result = _get_creative_goods_trade(start_year=2020, end_year=2020)
            self.assertEqual(result, {"type": "Error", "error": "CSV fetch failed"})

    def test_register_tool(self):
        """
        Test the registration of the get_creative_goods_trade tool.

        This test verifies that the register function correctly registers the tool
        with the FastMCP server and that the registered tool calls the underlying
        _get_creative_goods_trade function.
        """
        mock_mcp = MagicMock()

        # Call the register function
        register(mock_mcp)

        # Verify that mcp.tool was called with the correct description
        mock_mcp.tool.assert_called_once_with(
            description="Domestic Exports, Re-exports and Imports of Creative Goods in Hong Kong"
        )

        # Get the mock that represents the decorator returned by mcp.tool
        mock_decorator = mock_mcp.tool.return_value

        # Verify that the mock decorator was called once (i.e., the function was decorated)
        mock_decorator.assert_called_once()

        # The decorated function is the first argument of the first call to the mock_decorator
        decorated_function = mock_decorator.call_args[0][0]

        # Verify the name of the decorated function
        self.assertEqual(decorated_function.__name__, "get_creative_goods_trade")

        # Call the decorated function and verify it calls _get_creative_goods_trade
        with patch(
            "hkopenai.hk_recreation_mcp_server.tools.creative_goods_trade._get_creative_goods_trade"
        ) as mock_get_creative_goods_trade:
            decorated_function(start_year=2020, end_year=2021)
            mock_get_creative_goods_trade.assert_called_once_with(2020, 2021)