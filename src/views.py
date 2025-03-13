import json
from datetime import datetime, timedelta

import pandas as pd

from src.utils import common_information, exchange_rate, get_excel_df, get_price_stock, greeting, top_5_operations


def main(str_time):
    """принимает дату в формате строки YYYY-MM-DD HH:MM:SS и возвращает общую информацию в формате
    json о банковских транзакциях за период с начала месяца до этой даты"""
    data = get_excel_df("operations.xlsx")
    data_df = pd.DataFrame(data)
    date_obj = datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
    data_df["datetime"] = pd.to_datetime(data_df["Дата операции"], dayfirst=True)
    json_data = data_df[
        (data_df["datetime"] >= (date_obj - timedelta(days=date_obj.day - 1))) & (data_df["datetime"] <= date_obj)
    ]

    agg_dict = {
        "greetings": greetings(),
        "cards": common_information(json_data),
        "top_transactions": top_5_operations(json_data),
        "currency_rates": get_stock_price(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]),
        "stock_prices": exchange_rate(["USD", "EUR"]),
    }
    return json.dumps(agg_dict, ensure_ascii=False)
