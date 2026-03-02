from typing import Iterator, Dict, Any, Generator

def filter_by_currency(transactions: list[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданной валюте.
    """
    for transaction in transactions:
        operation_amount = transaction.get("operationAmount", {})
        currency_info = operation_amount.get("currency", {})
        if currency_info.get("code") == currency:
            yield transaction


def transaction_descriptions(transactions: list[Dict[str, Any]]) -> Generator[str, None, None]:
    """
    Генератор описаний транзакций.
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """
    Генератор номеров банковских карт.
    """
    for number in range(start, end + 1):
        card_str = str(number).zfill(16)
        formatted_card = " ".join([card_str[i:i+4] for i in range(0, 16, 4)])
        yield formatted_card
