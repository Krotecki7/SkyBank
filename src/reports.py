import json
import logging
import os
from datetime import date, datetime, time, timedelta
from functools import wraps
from typing import Any

import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
rel_file_path = os.path.join(current_dir, "../logs/utils.log")
abs_file_path = os.path.abspath(rel_file_path)

reports_logger = logging.getLogger("reports")
file_handler = logging.FileHandler(abs_file_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s, %(name)s, %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
reports_logger.addHandler(file_handler)
reports_logger.setLevel(logging.DEBUG)


def writing_report(filename="report"):
    """Декоратор указывающий файл записи данных"""

    def my_decorator(function):
        """Декоратор записи данных в файл"""

        @wraps(function)
        def inner(*args: Any, **kwargs: Any) -> Any:
            """Функция - обёртка"""
            result = function(*args, **kwargs)
            result.to_json(
                path_or_buf=f"{filename}.json",
                orient="records",
                indent=4,
                force_ascii=False,
            )
            return result

        return inner

    return my_decorator


def spending_by_weekday(transactions, date):
    """возвращает средние траты в каждый из дней недели за последние три месяца (от переданной даты)"""
    try:
        if date is None:
            date = datetime.now()
        else:
            date = datetime.strptime(date, "%Y-%m-%d")

        transactions["datetime"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
        transactions["day_name"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True).dt.day_name()
        df = transactions[
            (transactions["datetime"] >= (date + relativedelta(months=-3))) & (transactions["datetime"] <= date)
        ].groupby(by="day_name")
        print(df.head(10))
        reports_logger.info("Успешное формирование отчета о средних тратах.")
        return (df["Сумма платежа"].mean().abs().round(2)).to_json()
    except Exception as e:
        reports_logger.warning(f"!!!! Неудачное формирование отчета. Ошибка - {e}")

