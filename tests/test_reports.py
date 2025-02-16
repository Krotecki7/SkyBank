import json

import pandas as pd
import pytest
import logging

from src.reports import spending_by_category, writing_report


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
        "Transaction currency": [
            "RUB",
            "RUB",
            "RUB",
            "RUB",
            "RUB",
            "RUB",
            "RUB",
            "RUB",
            "RUB",
            "RUB",
            "RUB",
        ],
        "Payment amount": [
            -160.89,
            -64.00,
            -118.12,
            -564,
            -1.32,
            -500.00,
            -525.00,
            -681,
            -339.90,
            -1468.00,
            -110.00,
        ],
        "Payment currency": [
            "RUB",
            "RUB",
            "RUB",
            "RUB",
            "RUB",
            "RUB",
            "RUB",
            "RUB",
            "RUB",
            "RUB",
            "RUB",
        ],
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


def test_spending_by_category(test_df):
    """Тест вывода трат по категории"""
    new_df = spending_by_category(test_df, "Супермаркеты", "2021-12-31 14:46:24")
    sorted_list_category = new_df.to_dict(orient="records")
    assert sorted_list_category == [
        {
            "Transaction date": "31.12.2021",
            "Transaction amount": -160.89,
            "Category": "Супермаркеты",
        },
        {
            "Transaction date": "31.12.2021",
            "Transaction amount": -64.0,
            "Category": "Супермаркеты",
        },
        {
            "Transaction date": "31.12.2021",
            "Transaction amount": -118.12,
            "Category": "Супермаркеты",
        },
        {
            "Transaction date": "19.11.2021",
            "Transaction amount": -339.9,
            "Category": "Супермаркеты",
        },
    ]


def test_spending_by_category_with_incorrect_date(capsys, test_df):
    """Тест вывода сообщения при ошибке формата даты"""
    assert (spending_by_category(test_df, "Супермаркеты", "31-12-2021")).to_dict(
        orient="records"
    ) == []
    result = capsys.readouterr()
    assert result.out == "Некорректный формат даты\nФормирование отчёта завершено\n"


def test_spending_by_category_with_incorrect_category(capsys, test_df):
    """Тест вывода сообщения при ошибке ввода категории"""
    assert (
        spending_by_category(test_df, "Супермаркет", "2021-12-31 14:46:24")
    ).to_dict(orient="records") == []
    result = capsys.readouterr()
    assert result.out == "Неверно введена категория\nФормирование отчёта завершено\n"


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
