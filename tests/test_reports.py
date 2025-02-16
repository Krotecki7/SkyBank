import json

import pandas as pd
import pytest
import logging

from src.reports import spending_by_category, writing_report


def test_spending_by_category(test_df):
    """Тест вывода трат по категории"""
    new_df = spending_by_category(test_df, "Супермаркеты", "2021-12-31 14:46:24")
    sorted_list_category = new_df.to_dict(orient="records")
    assert sorted_list_category == [
        {"Transaction date": "31.12.2021", "Transaction amount": -160.89, "Category": "Супермаркеты"},
        {"Transaction date": "31.12.2021", "Transaction amount": -64.0, "Category": "Супермаркеты"},
        {"Transaction date": "31.12.2021", "Transaction amount": -118.12, "Category": "Супермаркеты"},
        {"Transaction date": "19.11.2021", "Transaction amount": -339.9, "Category": "Супермаркеты"},
    ]


def test_spending_by_category_with_incorrect_date(capsys, test_df):
    """Тест вывода сообщения при ошибке формата даты"""
    assert (spending_by_category(test_df, "Супермаркеты", "31-12-2021")).to_dict(orient="records") == []
    result = capsys.readouterr()
    assert result.out == "Некорректный формат даты\nФормирование отчёта завершено\n"


def test_spending_by_category_with_incorrect_category(capsys, test_df):
    """Тест вывода сообщения при ошибке ввода категории"""
    assert (spending_by_category(test_df, "Супермаркет", "2021-12-31 14:46:24")).to_dict(orient="records") == []
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
    assert result == [{"Запись 1": "тест1", "Запись 2": "тест1"}, {"Запись 1": "тест2", "Запись 2": "тест2"}]
