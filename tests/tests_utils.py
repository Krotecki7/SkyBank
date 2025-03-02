from unittest.mock import patch
import pytest
import pandas as pd

from src.utils import for_each_card, exchange_rate, greeting, max_five_transactions, read_excel


@patch("pandas.read_excel")
def test_read_excel(mock_read_excel, operations_from_excel, operations_list_valid):
    mock_read_excel.return_value = pd.DataFrame(operations_from_excel)
    result = read_excel("valid/path/to/file")

    assert operations_list_valid in result


def test_read_excel_empty_path():
    result = read_excel("")

    assert [] in result


@patch("pandas.read_excel")
def test_read_excel_empty_file(mock_read_excel):
    mock_read_excel.return_value = pd.DataFrame()
    result = read_excel("valid/path/to/file")

    assert [] in result


def test_read_excel_invalid_path():
    result = read_excel("invalid/path/to/file")

    assert [] in result


def test_greeting():
    current_hour = pd.Timestamp.now().hour
    day_time_now = greeting()

    if 0 <= current_hour < 6 or 22 <= current_hour <= 23:
        assert day_time_now == "Доброй ночи"
    elif 17 <= current_hour <= 22:
        assert day_time_now == "Добрый вечер"
    elif 7 <= current_hour <= 11:
        assert day_time_now == "Доброе утро"
    else:
        assert day_time_now == "Добрый день"


@patch("src.utils.requests.get")
def test_exchange_rate(mock_get, currencies, answer_currencies):
    """Тест при получении ответа от API"""
    mock_get.return_value.json.return_value = answer_currencies
    mock_get.return_value.status_code = 200
    assert exchange_rate(currencies) == [{"currency": "USD", "rate": 92.86}]


@patch("src.utils.requests.get")
def test_exchange_rate_with_incorrect_status_code(mock_get, currencies, answer_currencies):
    """Тест при отсутствии ответа от API"""
    mock_get.return_value.json.return_value = answer_currencies
    mock_get.return_value.status_code = 404
    assert exchange_rate(currencies) == []


def test_for_each_card(operations_list_valid, card_info_result):
    result = for_each_card(operations_list_valid)

    assert result == card_info_result


def test_for_each_card_empty_list():
    result = for_each_card([])

    assert result == []
