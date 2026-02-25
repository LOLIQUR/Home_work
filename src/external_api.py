"""
Модуль для работы с внешним API конвертации валют.
"""
import os
import requests
from typing import Dict, Any


def convert_to_ruble(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction: Словарь с данными о транзакции

    Returns:
        Сумма в рублях (float)
    """
    # Получаем информацию о валюте и сумме
    operation_amount = transaction.get("operationAmount", {})
    amount = float(operation_amount.get("amount", 0))
    currency = operation_amount.get("currency", {}).get("code", "RUB")

    # Если рубли - возвращаем как есть
    if currency == "RUB":
        return amount

    # Для USD и EUR конвертируем через API
    if currency in ["USD", "EUR"]:
        api_key = os.getenv("EXCHANGE_API_KEY")
        if not api_key:
            raise ValueError("API key not found")

        # Здесь будет запрос к API (пока заглушка)
        # TODO: Реализовать запрос к Exchange Rates Data API
        return amount * 90  # Временно: 1 USD/EUR = 90 RUB

    # Если неизвестная валюта - возвращаем 0
    return 0.0
