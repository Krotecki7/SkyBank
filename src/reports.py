import logging
import os
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Optional

import numpy as np
import pandas as pd

from src.utils import get_excel_df

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


def spending_by_category(transactions_df: pd.DataFrame, category: str, date: Optional[str] = None) -> dict:
    """Функция для вычисления трат по категории за последние три месяца."""

    if date is None:
        date = datetime.now()
    else:
        date = pd.to_datetime(date, dayfirst=False)

    three_months_ago = date - pd.DateOffset(months=3)

    filtered_df = transactions_df[
        (transactions_df["Категория"] == category)
        & (pd.to_datetime(transactions_df["Дата платежа"], dayfirst=False) >= three_months_ago)
        & (pd.to_datetime(transactions_df["Дата платежа"], dayfirst=False) <= date)
    ]

    total_expenses = filtered_df["Сумма платежа"].sum()
    return total_expenses
