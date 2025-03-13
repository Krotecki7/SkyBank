import json

import pandas as pd
import pytest

from src.reports import spending_by_weekday, writing_report


@pytest.fixture
def df_spendings():
    return pd.DataFrame(
        {
            "Дата операции": ["31.01.2022 16:44:00", "30.12.2021 16:44:00", "24.12.2021 16:44:00"],
            "Дата платежа": ["31.12.2021", "30.12.2021", "24.12.2021"],
            "Сумма операции": [-160.89, -400, -900],
            "Сумма платежа": [-160.89, -400, -900],
        }
    )


def test_spending_by_weekday_1(df_spendings):
    assert spending_by_weekday(df_spendings, "2022-02-01") is None


def test_writing_report():
    """Тест декоратора записывающего данные в указанный файл"""
    filename = "test_data"
    test_dict = {"Запись 1": ["тест1", "тест2"], "Запись 2": ["тест1", "тест2"]}

    @writing_report(filename)
    def func():
        return pd.DataFrame(test_dict)

    func()
    with open(f"{filename}.json", encoding="utf-8") as file:
        result = json.load(file)
    assert result == [
        {"Запись 1": "тест1", "Запись 2": "тест1"},
        {"Запись 1": "тест2", "Запись 2": "тест2"},
    ]
