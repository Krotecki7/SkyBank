from typing import Any

import pandas as pd
import pytest


@pytest.fixture
def currencies() -> list[str]:
    return ["USD"]


@pytest.fixture
def answer_currencies() -> dict[str, Any]:
    return {
        "base": "USD",
        "date": "2022-04-14",
        "rates": {"RUB": 92.86},
        "success": True,
        "timestamp": 1519296206,
    }


@pytest.fixture
def stocks() -> list[str]:
    return ["AAPL"]


@pytest.fixture
def answer_stocks() -> dict[str, Any]:
    return {
        "Meta Data": {
            "1. Information": "Daily Prices (open, high, low, close) and Volumes",
            "2. Symbol": "AAPL",
            "3. Last Refreshed": "2024-09-24",
            "4. Output Size": "Compact",
            "5. Time Zone": "US/Eastern",
        },
        "Time Series (Daily)": {
            "2024-09-24": {
                "1. open": "219.7800",
                "2. high": "221.1900",
                "3. low": "218.1600",
                "4. close": "220.9700",
                "5. volume": "3184114",
            },
            "2024-09-23": {
                "1. open": "218.0000",
                "2. high": "220.6200",
                "3. low": "217.2700",
                "4. close": "220.5000",
                "5. volume": "4074755",
            },
        },
    }


@pytest.fixture
def test_list_for_investment_bank() -> list[dict[str, Any]]:
    return [
        {"Transaction date": "31.12.2021 16:44:00", "Transaction amount": -160.89},
        {"Transaction date": "28.12.2021 18:24:02", "Transaction amount": -1840.0},
        {"Transaction date": "26.12.2021 20:39:43", "Transaction amount": -228.0},
        {"Transaction date": "26.12.2021 12:33:51", "Transaction amount": -34.0},
        {"Transaction date": "16.12.2021 15:01:10", "Transaction amount": -300.0},
        {"Transaction date": "20.11.2021 16:09:16", "Transaction amount": -19.99},
        {"Transaction date": "03.11.2021 13:03:16", "Transaction amount": -56.0},
        {"Transaction date": "06.10.2021 16:32:03", "Transaction amount": -94.82},
    ]
