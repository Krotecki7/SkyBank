from src.reports import spending_by_weekday
from src.services import find_numbers
from src.utils import common_information, greeting


def main():
    print(
        """1: Информация по карте
             2: Поиск по номеру телефона
             3: Информация о тратах за последние три месяца"""
    )
    user_input = input("Выберите, что бы вы хотели сделать")
    if user_input == "1":
        print(greeting())
        print(common_information(list_dict=get_excel_df("operations.xlsx")))
    elif user_input == "2":
        print(greeting())
        print(find_numbers(list_trans=get_excel_df("operations.xlsx")))
    elif user_input == "3":
        print(greeting())
        print(spending_by_weekday(transactions=get_excel_df("operations.xlsx")))
