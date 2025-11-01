"""
Модуль для работы с генераторами транзакций.
"""


def filter_by_currency(transactions, currency):
    """
    Фильтрует транзакции по заданной валюте.

    Args:
        transactions: Список словарей с транзакциями
        currency: Код валюты для фильтрации (например, "USD")

    Returns:
        Итератор, выдающий транзакции в заданной валюте
    """
    pass


def transaction_descriptions(transactions):
    """
    Генератор описаний транзакций.

    Args:
        transactions: Список словарей с транзакциями

    Yields:
        Описание каждой транзакции
    """
    pass


def card_number_generator(start, end):
    """
    Генератор номеров банковских карт.

    Args:
        start: Начальный номер карты
        end: Конечный номер карты

    Yields:
        Номера карт в формате XXXX XXXX XXXX XXXX
    """
    pass