import json
import os

from src.utils import exchange_rate, for_each_card, get_price_stock, greeting, read_excel, max_five_transactions

path_to_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.xlsx")
my_list = read_excel(path_to_file)


def return_json_answer(user_date):
    """Функция выводящая результат запроса по дате"""
    info_by_transactions = {
        "greeting": greeting(),
        "cards": for_each_card(my_list),
        "top transactions": max_five_transactions(user_date),
        "currency rates": exchange_rate(currency_list=["USD", "EUR"]),
        "stock_prices": get_price_stock(stocks=["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]),
    }
    answer_in_json_format = json.dumps(info_by_transactions, indent=4, ensure_ascii=False)
    return answer_in_json_format
