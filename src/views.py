import json

import pandas as pd

from src.utils import (exchange_rate, for_each_card, get_price_stock, greeting,
                       top_5_transactions)


def return_json_answer(data_frame: pd.DataFrame, date: str, user_settings):
    """Функция выводящая результат запроса по дате"""
    info_by_transactions = {
        "greeting": greeting(),
        "cards": for_each_card(my_list),
        "top transactions": top_5_transactions(date, data_frame),
        "currency rates": exchange_rate(user_settings["user_currencies"]),
        "stock_prices": get_price_stock(user_settings["user_stocks"]),
    }
    answer_in_json_format = json.dumps(
        info_by_transactions, indent=4, ensure_ascii=False
    )
    return answer_in_json_format
