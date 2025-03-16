import json

import pandas as pd
import pytest

from src.reports import spending_by_category, writing_report
from datetime import datetime


def test_spending_by_category():
    data = {
        'Категория': ['Еда', 'Еда', 'Транспорт', 'Развлечения', 'Еда'],
        'Дата платежа': [
            '2023-07-15',
            '2023-08-10',
            '2023-09-20',
            '2023-09-25',
            '2023-10-05'
        ],
        'Сумма платежа': [100, 150, 200, 50, 300]
    }

    transactions_df = pd.DataFrame(data)

    result = spending_by_category(transactions_df, 'Еда', '2023-10-10')
    assert result == 550

    result = spending_by_category(transactions_df, 'Транспорт', '2023-10-10')
    assert result == 200

    result = spending_by_category(transactions_df, 'Развлечения', '2023-10-10')
    assert result == 50

    result = spending_by_category(transactions_df, 'Косметика', '2023-10-10')
    assert result == 0

    result = spending_by_category(transactions_df, 'Еда', '2023-09-30')
    assert result == 250


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
