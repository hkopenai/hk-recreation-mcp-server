import unittest
from unittest.mock import patch
from hkopenai.hk_recreation_mcp_server.tool_creative_goods_trade import (
    fetch_creative_goods_data,
    get_creative_goods_trade
)

class TestCreativeGoodsTrade(unittest.TestCase):
    CSV_DATA = """Year,CI_Goods_Cat,Trade_Type,Values,Percentage,Last Update
2025,1,1,47873,999.9%,31/03/2025
2025,2,1,177,999.9%,31/03/2025
2025,3,1,11648944,999.9%,31/03/2025
2024,1,2,43547,999.9%,31/03/2024
2024,2,2,686423,999.9%,31/03/2024
2023,1,3,45383,999.9%,31/03/2023
2023,2,3,982377,999.9%,31/03/2023"""

    def setUp(self):
        self.mock_requests = patch('requests.get').start()
        mock_response = self.mock_requests.return_value
        mock_response.text = self.CSV_DATA
        mock_response.encoding = 'utf-8'
        self.addCleanup(patch.stopall)

    def test_fetch_creative_goods_data(self):
        result = fetch_creative_goods_data()
        self.assertEqual(len(result), 7)
        self.assertEqual(result[0]['Year'], '2025')
        self.assertEqual(result[3]['CI_Goods_Cat'], '1')
        self.assertEqual(result[5]['Trade_Type'], '3')

    def test_get_creative_goods_trade(self):
        # Test without year filter
        result = get_creative_goods_trade()
        self.assertEqual(len(result), 7)
        self.assertEqual(result[0]['year'], 2025)
        self.assertEqual(result[0]['category'], "Advertising")
        self.assertEqual(result[3]['trade_type'], "Re-exports")

        # Test with year filter
        result = get_creative_goods_trade(start_year=2024, end_year=2024)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['year'], 2024)
        self.assertEqual(result[1]['trade_type_code'], 2)

    def test_special_values(self):
        result = get_creative_goods_trade()
        for item in result:
            # All test data has 999.9% which should be converted to None
            self.assertIsNone(item['percentage'])
            # Values should be converted to int except special cases
            self.assertTrue(isinstance(item['value'], int) or item['value'] is None)

if __name__ == "__main__":
    unittest.main()
