from unittest.mock import patch

import pandas as pd
import pytest

from src.utils import exchange_rate, greeting, top_5_operations, common_information, get_excel_df


@pytest.fixture
def currencies():
    return ["USD"]


@pytest.fixture
def answer_currencies():
    return {"base": "USD", "rates": {"RUB": "92.86"}}


@pytest.fixture
def get_excel_return():
    return [
        {
            "Дата операции": "16.07.2019 16:30:10",
            "Дата платежа": "18.07.2019",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -49.8,
            "Валюта операции": "RUB",
            "Сумма платежа": -49.8,
            "Валюта платежа": "RUB",
            "Кэшбэк": 4,
            "Категория": "Супермаркеты",
            "MCC": 5411.0,
            "Описание": "SPAR",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 49.8,
        },
        {
            "Дата операции": "16.07.2019 16:13:54",
            "Дата платежа": "17.07.2019",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -114.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -114.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": 2,
            "Категория": "Фастфуд",
            "MCC": 5814.0,
            "Описание": "IP Yakubovskaya M. V.",
            "Бонусы (включая кэшбэк)": 2,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 114.0,
        },
        {
            "Дата операции": "16.07.2019 13:27:53",
            "Дата платежа": "17.07.2019",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -148.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -148.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": 10,
            "Категория": "Транспорт",
            "MCC": 4121.0,
            "Описание": "Яндекс Такси",
            "Бонусы (включая кэшбэк)": 2,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 148.0,
        },
    ]


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


@patch("pandas.read_excel")
def test_get_excel_df_1(mock_get, get_excel_return):
    mock_get.return_value = pd.DataFrame(
        [
            {
                "Дата операции": "16.07.2019 16:30:10",
                "Дата платежа": "18.07.2019",
                "Номер карты": "*7197",
                "Статус": "OK",
                "Сумма операции": -49.8,
                "Валюта операции": "RUB",
                "Сумма платежа": -49.8,
                "Валюта платежа": "RUB",
                "Кэшбэк": 4,
                "Категория": "Супермаркеты",
                "MCC": 5411.0,
                "Описание": "SPAR",
                "Бонусы (включая кэшбэк)": 0,
                "Округление на инвесткопилку": 0,
                "Сумма операции с округлением": 49.8,
            },
            {
                "Дата операции": "16.07.2019 16:13:54",
                "Дата платежа": "17.07.2019",
                "Номер карты": "*7197",
                "Статус": "OK",
                "Сумма операции": -114.0,
                "Валюта операции": "RUB",
                "Сумма платежа": -114.0,
                "Валюта платежа": "RUB",
                "Кэшбэк": 2,
                "Категория": "Фастфуд",
                "MCC": 5814.0,
                "Описание": "IP Yakubovskaya M. V.",
                "Бонусы (включая кэшбэк)": 2,
                "Округление на инвесткопилку": 0,
                "Сумма операции с округлением": 114.0,
            },
            {
                "Дата операции": "16.07.2019 13:27:53",
                "Дата платежа": "17.07.2019",
                "Номер карты": "*7197",
                "Статус": "OK",
                "Сумма операции": -148.0,
                "Валюта операции": "RUB",
                "Сумма платежа": -148.0,
                "Валюта платежа": "RUB",
                "Кэшбэк": 10,
                "Категория": "Транспорт",
                "MCC": 4121.0,
                "Описание": "Яндекс Такси",
                "Бонусы (включая кэшбэк)": 2,
                "Округление на инвесткопилку": 0,
                "Сумма операции с округлением": 148.0,
            },
        ]
    )
    assert get_excel_df("filename.xlsx") == get_excel_return


@patch("pandas.read_excel")
def test_get_excel_df_2(mock_get):
    mock_get.return_value = pd.DataFrame({})
    assert get_excel_df("filename.xlsx") == []


@patch("os.path.join")
def test_get_excel_df_4(mock_path):
    mock_path.return_value = None
    assert get_excel_df("filename.xlsx") is None


def test_top_5_operations_1(get_excel_return):
    assert top_5_operations(get_excel_return) == [
        {
            "date": "16.07.2019 16:30:10",
            "card_number": "*7197",
            "amount": -49.8,
            "category": "Супермаркеты",
            "descriprion": "SPAR",
        },
        {
            "date": "16.07.2019 16:13:54",
            "card_number": "*7197",
            "amount": -114.0,
            "category": "Фастфуд",
            "descriprion": "IP Yakubovskaya M. V.",
        },
        {
            "date": "16.07.2019 13:27:53",
            "card_number": "*7197",
            "amount": -148.0,
            "category": "Транспорт",
            "descriprion": "Яндекс Такси",
        },
    ]


def test_top_5_operations_2(get_excel_return):
    assert top_5_operations(None) == []


def test_common_information_1(get_excel_return):
    assert common_information(get_excel_return) == [{"last_digits": "7197", "total_spent": 311.8, "cashbak": 5.13}]


def test_common_information_2():
    assert common_information([]) is None


def test_common_information_3():
    assert common_information(None) is None


def test_common_information_4():
    assert common_information(None) is None
