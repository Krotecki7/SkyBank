from datetime import datetime
import logging
import os
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd

path_to_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.xlsx")

current_dir = os.path.dirname(os.path.abspath(__file__))
rel_file_path = os.path.join(current_dir, "../logs/utils.log")
abs_file_path = os.path.abspath(rel_file_path)

reports_logger = logging.getLogger("reports")
file_handler = logging.FileHandler(abs_file_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s, %(name)s, %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
reports_logger.addHandler(file_handler)
reports_logger.setLevel(logging.DEBUG)


def writing_report(filename="report") -> Callable:
    """Декоратор указывающий файл записи данных"""

    def my_decorator(function: Callable) -> Callable:
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


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция принимает на вход датафрейм с транзакциями, название категории, и опциональную дату в формате ДД.ММ.ГГГГ.
    Если дата не передана, то берется текущая дата.
    И возвращает траты по заданной категории за последние три месяца (от переданной даты).
    """
    try:
        if not date:
            stop_date = datetime.now()

        else:
            stop_date = datetime.strptime(date, "%d.%m.%Y")

        reports_logger.info("Определение даты, начиная с которой будут взяты операции для подсчета трат по категориям")

        start_date = stop_date - pd.timedelta(days=90)

        reports_logger.info("Проверка на наличие необходимых столбцов в датафрейм")

        required_columns = ["Дата платежа", "Категория", "Сумма операции"]
        for column in required_columns:

            if column not in transactions.columns:
                reports_logger.error(f"Отсутствует необходимый столбец: {column}")

                return pd.DataFrame()

        reports_logger.info("Преобразование дат операций в объект datatime")

        transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y")

        reports_logger.info("Формирование списка операций для формирования отчета")

        filtered_transactions = transactions[
            (transactions["Дата платежа"] >= start_date)
            & (transactions["Дата платежа"] <= stop_date)
            & (transactions["Категория"] == category)
            & (transactions["Сумма операции"] < 0)
        ]

        reports_logger.info("Инициализация отчета")

        total_spending = filtered_transactions["Сумма операции"].abs().sum()

        result = pd.DataFrame({"Категория": [category], "Сумма трат": [total_spending]})

    except ValueError as ve:
        reports_logger.error(f"Ошибка значения: {ve}")
        return pd.DataFrame()

    except Exception as e:
        reports_logger.error(f"Произошла ошибка: {e}")
        return pd.DataFrame()

    return result
