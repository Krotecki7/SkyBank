import datetime
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
    """Функция выводящая траты за последние 3 месяца от вводимой даты в заданой категории"""
    edit_df = transactions.drop(
        [
            "Payment date",
            "Card number",
            "Status",
            "Transaction currency",
            "Payment amount",
            "Payment currency",
            "Cashback",
            "MCC",
            "Description",
            "Bonuses (including cashback)",
            "Rounding to the investment bank",
            "The amount of the operation with rounding",
        ],
        axis=1,
    )
    edit_df["Transaction date"] = edit_df["Transaction date"].apply(
        lambda x: datetime.datetime.strptime(f"{x}", "%d.%m.%Y %H:%M:%S").date()
    )
    try:
        if date:
            end_date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date()
            start_date_obj = end_date_obj - datetime.timedelta(days=90)
        else:
            end_date_obj = datetime.datetime.now().date()
            start_date_obj = end_date_obj - datetime.timedelta(days=90)
        report_df = edit_df.loc[
            (edit_df["Transaction date"] <= end_date_obj)
            & (edit_df["Transaction date"] >= start_date_obj)
            & (edit_df["Category"] == category)
        ]
        report_df.loc[:, "Transaction date"] = report_df["Transaction date"].apply(lambda x: x.strftime("%d.%m.%Y"))
        if not report_df.to_dict(orient="records"):
            raise NameError
    except ValueError:
        reports_logger.error("Ошибка в выборке операций: не корректный формат даты")
        print("Некорректный формат даты")
        return pd.DataFrame({})
    except NameError:
        print("Неверно введена категория")
        return pd.DataFrame({})
    else:
        reports_logger.info("Выборка операций успешно завершена")
        return report_df
    finally:
        reports_logger.info("Завершение работы программы")
        print("Формирование отчёта завершено")
