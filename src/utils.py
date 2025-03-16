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


def get_excel_df(filename: str) -> list[dict]:
    """считывает данные из внешнего файла Excel и возвращает их в формате DataFrame
    за период с начала месяца до заданной даты в формате YYYY-MM-DD HH:MM:SS"""
    try:
        path = os.path.join("../data/", filename)
        excel_data = pd.read_excel(path)
        list_dict = excel_data.to_dict(orient="records")
        utils_logger.info(f"Успешное преобразование файла {filename} из объекта json в python")
        return list_dict
    except Exception as e:
        utils_logger.warning(f"!!!! Не удалось преобразовать файл {filename} из объекта json в python. Ошибка - {e}")


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


def top_5_operations(list_dict):
    """возвращает 5 самых крупных операции по столбцу "Сумма операции"""
    try:
        list_data = []
        df = pd.DataFrame(list_dict)
        df["datetime"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
        df_sorted = df.sort_values(by="Сумма платежа", ascending=False, inplace=False).iloc[0:5, :]
        for _, row in df_sorted.iterrows():
            dic = {
                "date": row["Дата операции"],
                "card_number": row["Номер карты"],
                "amount": row["Сумма операции"],
                "category": row["Категория"],
                "descriprion": row["Описание"],
            }
            list_data.append(dic)
        utils_logger.info("Успешно сформированы 5 самых доходных операций")
        return list_data[:6]
    except Exception as e:
        utils_logger.warning(
            f"""!!!! Не удалось сформировать отчет проверьте поля списка {list_dict}.
        Ошибка - {e}"""
        )
        return []


def common_information(list_dict):
    """возвращает общую информацию по всем транзакциям"""
    try:
        list_data = []
        df = pd.DataFrame(list_dict)
        df["datetime"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
        grouped_data = df.groupby("Номер карты").agg({"Сумма платежа": "sum", "Кэшбэк": "sum"}).reset_index()
        grouped_data["Сумма платежа"] = grouped_data["Сумма платежа"].abs()
        for _, row in grouped_data.iterrows():
            dic = {
                "last_digits": (row["Номер карты"])[-4:],
                "total_spent": row["Сумма платежа"],
                "cashbak": round((row["Кэшбэк"]) / (row["Сумма платежа"]) * 100, 2),
            }
            list_data.append(dic)
        utils_logger.info("Успешно сформированa общая информация по всем транзакциям")
        return list_data
    except Exception as e:
        utils_logger.warning(
            f"""!!!! Не удалось сформировать отчет проверьте поля списка {list_dict}.
        Ошибка - {e}"""
        )
