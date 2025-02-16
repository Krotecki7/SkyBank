from unittest.mock import patch

import pytest
import logging

from src.utils import card_info, exchange_rate, greeting, top_5_transactions


def test_greeting():
    """Тест вывода приветсвия в зависимости от текущего времени"""
    with freeze_time("2024-09-30 16:39:11"):
        assert greeting() == "Добрый день"
    with freeze_time("2024-09-30 08:39:11"):
        assert greeting() == "Доброе утро"
    with freeze_time("2024-09-30 19:39:11"):
        assert greeting() == "Добрый вечер"
    with freeze_time("2024-09-30 03:39:11"):
        assert greeting() == "Доброй ночи"


@patch("src.utils.requests.get")
def test_exchange_rate(mock_get, currencies, answer_currencies):
    """Тест при получении ответа от API"""
    mock_get.return_value.json.return_value = answer_currencies
    mock_get.return_value.status_code = 200
    assert exchange_rate(currencies) == [{"currency": "USD", "rate": 92.86}]


@patch("src.utils.requests.get")
def test_exchange_rate_with_incorrect_status_code(
    mock_get, currencies, answer_currencies
):
    """Тест при отсутствии ответа от API"""
    mock_get.return_value.json.return_value = answer_currencies
    mock_get.return_value.status_code = 404
    assert exchange_rate(currencies) == []


def test_card_info(test_df):
    """Тест корректности работы функции"""
    assert card_info("2021-12-31 16:44:00", test_df) == [
        {"Card number": "5091", "Transaction amount": -1589.0, "cashback": 15.89},
        {"Card number": "7197", "Transaction amount": -344.33, "cashback": 3.44},
    ]


def test_card_info_incorrect_date_format(test_df):
    """Тест функции с некорректным форматом даты"""
    assert card_info("21.12.2021 16:44:00", test_df) == []


def test_top_5_transactions(test_df):
    """Тест топ 5 транзакций за месяц"""
    assert top_5_transactions("2021-12-31 16:44:00", test_df) == [
        {
            "date": "31.12.2021",
            "amount": -564.0,
            "category": "Различные товары",
            "description": "Константин. К",
        },
        {
            "date": "09.12.2021",
            "amount": -525.0,
            "category": "Одежда и обувь",
            "description": "WILDBERRIES",
        },
        {
            "date": "16.12.2021",
            "amount": -500.0,
            "category": "Местный транспорт",
            "description": "Метро Санкт-петербург",
        },
        {
            "date": "31.12.2021",
            "amount": -160.89,
            "category": "Супермаркеты",
            "description": "Колхоз",
        },
        {
            "date": "31.12.2021",
            "amount": -118.12,
            "category": "Супермаркеты",
            "description": "Магнит",
        },
    ]


def test_top_5_transactions_with_incorrect_date_format(test_df):
    """Тест топа транзакций при некорректном формате даты"""
    assert top_5_transactions("2021.12.31 16:44:00", test_df) == []
