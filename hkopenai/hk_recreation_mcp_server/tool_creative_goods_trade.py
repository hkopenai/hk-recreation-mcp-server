"""
Module for fetching and processing creative goods trade data in Hong Kong.
This module provides tools to retrieve and format data related to domestic exports,
re-exports, and imports of creative goods.
"""

import requests
import csv
from io import StringIO
from typing import List, Dict, Optional
from pydantic import Field
from typing_extensions import Annotated

# Mapping dictionaries
CATEGORY_MAP = {
    1: "Advertising",
    2: "Architecture",
    3: "Design",
    4: "Digital Entertainment",
    5: "Film & Television",
    6: "Music",
    7: "Printing & Publishing",
    8: "Overall Creative Goods",
}

TRADE_TYPE_MAP = {1: "Domestic Exports", 2: "Re-exports", 3: "Imports"}


def fetch_creative_goods_data() -> List[Dict]:
    """Fetch creative goods trade data from CCID website"""
    url = "https://www.ccidahk.gov.hk/data/SCG_TradeTOT.csv"
    response = requests.get(url)
    response.encoding = "utf-8"
    reader = csv.DictReader(StringIO(response.text))
    return list(reader)


def get_creative_goods_trade(
    start_year: Annotated[
        Optional[int], Field(description="Start year of range")
    ] = None,
    end_year: Annotated[Optional[int], Field(description="End year of range")] = None,
) -> List[Dict]:
    """Get Domestic Exports, Re-exports and Imports of Creative Goods in Hong Kong

    Args:
        start_year: Optional start year filter
        end_year: Optional end year filter

    Returns:
        List of trade records with mapped category/trade type names and cleaned values
    """
    data = fetch_creative_goods_data()

    # Filter by year range if provided
    if start_year or end_year:
        data = [
            row
            for row in data
            if (not start_year or int(row["Year"]) >= start_year)
            and (not end_year or int(row["Year"]) <= end_year)
        ]

    # Process and clean data
    processed = []
    for row in data:
        processed_row = {
            "year": int(row["Year"]),
            "category_code": int(row["CI_Goods_Cat"]),
            "category": CATEGORY_MAP.get(int(row["CI_Goods_Cat"])),
            "trade_type_code": int(row["Trade_Type"]),
            "trade_type": TRADE_TYPE_MAP.get(int(row["Trade_Type"])),
            "value": (
                None
                if row["Values"] in ("999999998", "999999999")
                else int(row["Values"])
            ),
            "percentage": (
                None
                if row["Percentage"] in ("999.8%", "999.9%")
                else float(row["Percentage"].rstrip("%"))
            ),
        }
        processed.append(processed_row)

    return processed
