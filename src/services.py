import json
import logging
import os
import re

path_to_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.xlsx")

current_dir = os.path.dirname(os.path.abspath(__file__))
rel_file_path = os.path.join(current_dir, "../logs/utils.log")
abs_file_path = os.path.abspath(rel_file_path)

services_logger = logging.getLogger("services")
file_handler = logging.FileHandler(abs_file_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s, %(name)s, %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
services_logger.addHandler(file_handler)
services_logger.setLevel(logging.DEBUG)


def find_numbers(list_trans):
    """Функция возвращает JSON со всеми транзакциями, содержащими в описании мобильные номера."""
    current_transactions = []
    for transaction in list_trans:
        pattern = r"[+]\d"
        description = transaction.get("Описание")
        if re.findall(pattern, str(description), flags=re.IGNORECASE):
            current_transactions.append(transaction)
    services_logger.debug("Получены транзакции с номерами телефонов в описании")
    current_transactions_1 = json.dumps(current_transactions, ensure_ascii=False)
    return current_transactions_1
