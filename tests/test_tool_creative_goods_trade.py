"""
Module for testing the creative goods trade data fetching and processing.
This module contains unit tests to verify the functionality of the creative goods trade tools.
"""

import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_recreation_mcp_server.tool_creative_goods_trade import (
    fetch_creative_goods_data,
    _get_creative_goods_trade,
    register,
)


class TestCreativeGoodsTrade(unittest.TestCase):
    """
    Test class for verifying the functionality of creative goods trade data processing.
    This class tests data fetching and processing logic with mocked CSV data.
    """

    CSV_DATA = """Year,CI_Goods_Cat,Trade_Type,Values,Percentage,Last Update
2025,1,1,47873,999.9%,31/03/2025
2025,2,1,177,999.9%,31/03/2025
2025,3,1,11648944,999.9%,31/03/2025
2024,1,2,43547,999.9%,31/03/2024
2024,2,2,686423,999.9%,31/03/2024
2023,1,3,45383,999.9%,31/03/2023
2023,2,3,982377,999.9%,31/03/2023"""

    def setUp(self):
        """
        Set up test fixtures before each test method.
        Mocks the requests.get method to return predefined CSV data for testing.
        """
        self.mock_requests = patch("requests.get").start()
        mock_response = self.mock_requests.return_value
        mock_response.text = self.CSV_DATA
        mock_response.encoding = "utf-8"
        self.addCleanup(patch.stopall)

    def test_fetch_creative_goods_data(self):
        """
        Test fetching creative goods data from a mocked CSV source.
        Verifies the correct number of records and specific field values.
        """
        result = fetch_creative_goods_data()
        self.assertEqual(len(result), 7)
        self.assertEqual(result[0]["Year"], "2025")
        self.assertEqual(result[3]["CI_Goods_Cat"], "1")
        self.assertEqual(result[5]["Trade_Type"], "3")

    def test_get_creative_goods_trade(self):
        """
        Test processing creative goods trade data with and without year filters.
        Verifies the correct mapping of categories and trade types, and filtering by year.
        """
        # Test without year filter
        result = _get_creative_goods_trade()
        self.assertEqual(len(result), 7)
        self.assertEqual(result[0]["year"], 2025)
        self.assertEqual(result[0]["category"], "Advertising")
        self.assertEqual(result[3]["trade_type"], "Re-exports")

        # Test with year filter
        result = _get_creative_goods_trade(start_year=2024, end_year=2024)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["year"], 2024)
        self.assertEqual(result[1]["trade_type_code"], 2)

    def test_special_values(self):
        """
        Test handling of special values in creative goods trade data.
        Verifies that special percentage values are converted to None and values are integers.
        """
        result = _get_creative_goods_trade()
        for item in result:
            # All test data has 999.9% which should be converted to None
            self.assertIsNone(item["percentage"])
            # Values should be converted to int except special cases
            self.assertTrue(isinstance(item["value"], int) or item["value"] is None)

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
            "hkopenai.hk_recreation_mcp_server.tool_creative_goods_trade._get_creative_goods_trade"
        ) as mock_get_creative_goods_trade:
            decorated_function(start_year=2020, end_year=2021)
            mock_get_creative_goods_trade.assert_called_once_with(2020, 2021)


if __name__ == "__main__":
    unittest.main()
