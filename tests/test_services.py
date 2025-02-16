from src.services import find_numbers
import logging


def test_find_numbers(number):
    assert find_numbers("966") == number
