import datetime
import logging
import os

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

API_ALFA = os.getenv("API_KEY_ALFA")
API_LAYER = os.getenv("API_KEY_LAYER")

current_dir = os.path.dirname(os.path.abspath(__file__))
rel_file_path = os.path.join(current_dir, "../logs/utils.log")
abs_file_path = os.path.abspath(rel_file_path)

utils_logger = logging.getLogger("utils")
file_handler = logging.FileHandler(abs_file_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s, %(name)s, %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
utils_logger.addHandler(file_handler)
utils_logger.setLevel(logging.DEBUG)

path_to_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.xlsx")


def greeting():
    """
    Функция, которая приветствует в зависимости от текущего времени суток.
    Возвращает строку приветствия в зависимости от времени.
    """
    current_date_time = datetime.datetime.now()
    hour = current_date_time.hour

    if 0 <= hour < 6 or 22 <= hour <= 23:
        return "Доброй ночи"
    elif 17 <= hour <= 22:
        return "Добрый вечер"
    elif 7 <= hour <= 11:
        return "Доброе утро"
    else:
        return "Добрый день"


def read_excel(path_to_file: str) -> list[dict]:
    """Функция читает .xlsx файл и возвращает список словарей"""
    df = pd.read_excel(path_to_file)
    result = df.apply(
        lambda row: {
            "Дата платежа": row["Дата платежа"],
            "Статус": row["Статус"],
            "Сумма платежа": row["Сумма платежа"],
            "Валюта платежа": row["Валюта платежа"],
            "Категория": row["Категория"],
            "Описание": row["Описание"],
            "Номер карты": row["Номер карты"],
        },
        axis=1,
    ).tolist()
    return result


my_list = read_excel(path_to_file)


def for_each_card(my_list: list) -> list:
    """Функция создания информации по каждой карте"""
    utils_logger.info("Начало работы функции (for_each_card)")
    cards = {}
    result = []
    utils_logger.info("Перебор транзакций")
    for i in my_list:
        if i["Номер карты"] == "nan" or type(i["Номер карты"]) is float:
            continue
        elif i["Сумма платежа"] == "nan":
            continue
        else:
            if i["Номер карты"][1:] in cards:
                cards[i["Номер карты"][1:]] += float(str(i["Сумма платежа"])[1:])
            else:
                cards[i["Номер карты"][1:]] = float(str(i["Сумма платежа"])[1:])
    for k, v in cards.items():
        result.append(
            {
                "last_digits": k,
                "total_spent": round(v, 2),
                "cashback": round(v / 100, 2),
            }
        )
    utils_logger.info("Завершение работы функции (for_each_card)")
    return result


stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]


def get_price_stock(stocks: list) -> list:
    """Функция для получения данных об акциях из списка S&P500"""
    utils_logger.info("Начало работы функции (get_price_stock)")
    api_key = API_ALFA
    stock_prices = []
    utils_logger.info("Функция обрабатывает данные транзакций.")
    for stock in stocks:
        utils_logger.info("Перебор акций в списке 'stocks' в функции (get_price_stock)")
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}"
        r = requests.get(url)
        result = r.json()

        stock_prices.append(
            {
                "stock": stock,
                "price": round(float(result["Global Quote"]["05. price"]), 2),
            }
        )
    utils_logger.info("Функция get_price_stock успешно завершила свою работу")
    return stock_prices


currency_list = ["USD", "EUR"]


def exchange_rate(currency_list: list[str]) -> list[dict[str, [str | int]]]:
    """Функция получения курса валют через API"""
    url = "https://api.apilayer.com/exchangerates_data/latest"
    headers = {"apikey": f"{API_LAYER}"}
    currency_rate = []
    for currency in currency_list:
        payload = {"symbols": "RUB", "base": f"{currency}"}
        response = requests.get(url, headers=headers, params=payload)
        status_code = response.status_code
        if status_code == 200:
            res = response.json()
            currency_rate_dict = {
                "currency": f"{res["base"]}",
                "rate": round(float(res["rates"]["RUB"]), 2),
            }
            currency_rate.append(currency_rate_dict)
        else:
            print("Запрос не был успешным.")
            utils_logger.warning("Запрос не удался")
            return []
    utils_logger.info("Данные по курсу валют успешно получены")
    return currency_rate


def max_five_transactions(data_time: pd.Timestamp) -> pd.DataFrame:
    """
    Функция, которая извлекает топ-5 транзакций по сумме платежа.
    """
    df = pd.read_excel(path_to_file)

    filtered_df = df.copy()

    filtered_df = filtered_df.loc[
        (pd.to_datetime(filtered_df["Дата операции"], format="%d.%m.%Y %H:%M:%S", dayfirst=True) <= data_time)
        & (
            pd.to_datetime(filtered_df["Дата операции"], format="%d.%m.%Y %H:%M:%S", dayfirst=True)
            >= data_time.replace(day=1)
        )
    ]
    top_transactions = filtered_df.sort_values(by="Сумма операции с округлением", ascending=False).head(5)
    return top_transactions
