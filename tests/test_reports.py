import json


import pandas as pd
import pytest

from src.reports import spending_by_category, writing_report


@pytest.mark.parametrize(
    "df, expected",
    [
        (
            pd.DataFrame(
                {
                    "Дата платежа": ["01.01.2025", "01.01.2025", "02.01.2025", "03.01.2025"],
                    "Категория": ["Такси", "Еда", "Такси", "Супермаркеты"],
                    "Сумма операции": [-777, -555, -1312, -666],
                }
            ),
            pd.DataFrame({"Категория": ["Еда"], "Сумма трат": [555]}),
        )
    ],
)
def test_spending_by_category(df, expected):
    result = spending_by_category(df, "Еда", "01.01.2025")
    pd.testing.assert_frame_equal(result, expected)


@pytest.mark.parametrize(
    "df, expected",
    [
        (
            pd.DataFrame(
                {
                    "Дата платежа": ["01.01.2025", "01.01.2025", "02.01.2025", "03.01.2025"],
                    "Категория": ["Такси", "Еда", "Такси", "Супермаркеты"],
                    "Сумма операции": [-777, -555, -1312, -666],
                }
            ),
            pd.DataFrame({"Категория": ["Еда"], "Сумма трат": [555]}),
        )
    ],
)
def test_spending_by_category_not_date(df, expected):
    result = spending_by_category(df, "Еда")
    pd.testing.assert_frame_equal(result, expected)


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
