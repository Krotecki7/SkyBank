from typing import Any

import pandas as pd
import pytest


@pytest.fixture
def currencies() -> list[str]:
    return ["USD"]


@pytest.fixture
def answer_currencies() -> dict[str, Any]:
    return {"base": "USD", "date": "2022-04-14", "rates": {"RUB": 92.86}, "success": True, "timestamp": 1519296206}


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
def test_df() -> pd.DataFrame:
    """Тестовый DataFrame"""
    test_dict = {
        "Transaction date": [
            "31.12.2021 16:44:00",
            "31.12.2021 16:42:04",
            "31.12.2021 16:39:04",
            "31.12.2021 01:23:42",
            "30.12.2021 19:06:39",
            "16.12.2021 11:26:30",
            "09.12.2021 08:50:35",
            "25.11.2021 20:29:13",
            "19.11.2021 18:54:29",
            "28.10.2021 15:56:36",
            "16.09.2021 12:55:33",
        ],
        "Payment date": [
            "31.12.2021",
            "31.12.2021",
            "31.12.2021",
            "31.12.2021",
            "31.12.2021",
            "18.12.2021",
            "09.12.2021",
            "25.11.2021",
            "19.11.2021",
            "28.10.2021",
            "16.09.2021",
        ],
        "Card number": [
            "*7197",
            "*7197",
            "*7197",
            "*5091",
            "*7197",
            "*5091",
            "*5091",
            "*4556",
            "*4556",
            "*7197",
            "*7197",
        ],
        "Status": ["OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK"],
        "Transaction amount": [
            -160.89,
            -64.00,
            -118.12,
            -564.0,
            -1.32,
            -500.00,
            -525.00,
            -681,
            -339.90,
            -1468.00,
            -110.00,
        ],
        "Transaction currency": ["RUB", "RUB", "RUB", "RUB", "RUB", "RUB", "RUB", "RUB", "RUB", "RUB", "RUB"],
        "Payment amount": [-160.89, -64.00, -118.12, -564, -1.32, -500.00, -525.00, -681, -339.90, -1468.00, -110.00],
        "Payment currency": ["RUB", "RUB", "RUB", "RUB", "RUB", "RUB", "RUB", "RUB", "RUB", "RUB", "RUB"],
        "Cashback": [None, None, None, None, 70, None, None, None, None, None, None],
        "Category": [
            "Супермаркеты",
            "Супермаркеты",
            "Супермаркеты",
            "Различные товары",
            "Каршеринг",
            "Местный транспорт",
            "Одежда и обувь",
            "Аптеки",
            "Супермаркеты",
            "Дом и ремонт",
            "Фастфуд",
        ],
        "MCC": [5411, 5411, 5411, 5411, 5411, 4111, 5651, 5912, 5411, 5200, 5814],
        "Description": [
            "Колхоз",
            "Колхоз",
            "Магнит",
            "Константин. К",
            "Ситидрайв",
            "Метро Санкт-петербург",
            "WILDBERRIES",
            "Аптека Вита",
            "Перекрёсток",
            "Леруа Мерлен",
            "Mouse Tail",
        ],
        "Bonuses (including cashback)": [3, 1, 2, 5, 0, 5, 5, 34, 16, 4, 2],
        "Rounding to the investment bank": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "The amount of the operation with rounding": [
            160.89,
            64.00,
            118.12,
            564,
            1.32,
            500.00,
            525.00,
            681,
            339.90,
            1468.00,
            110.00,
        ],
    }
    return pd.DataFrame(test_dict)


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
