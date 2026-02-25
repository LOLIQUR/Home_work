"""
Модуль для работы с внешним API конвертации валют.
"""
import os
import requests
from dotenv import load_dotenv
from typing import Dict, Any

# Загружаем переменные окружения из .env файла
load_dotenv()


def get_exchange_rate(base_currency: str) -> float:
    """
    Получает курс валюты к рублю через API.

    Args:
        base_currency: Базовая валюта (USD или EUR)

    Returns:
        Курс валюты к рублю
    """
    api_key = os.getenv("EXCHANGE_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Check your .env file.")

    url = f"http://api.exchangeratesapi.io/v1/latest"
    params = {
        "access_key": api_key,
        "base": base_currency,
        "symbols": "RUB"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data.get("success"):
            raise ValueError(f"API error: {data.get('error', {}).get('info', 'Unknown error')}")

        rub_rate = data["rates"].get("RUB")
        if not rub_rate:
            raise ValueError(f"RUB rate not found for {base_currency}")

        return rub_rate

    except requests.RequestException as e:
        raise ValueError(f"Failed to fetch exchange rate: {str(e)}")


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
        try:
            rate = get_exchange_rate(currency)
            return amount * rate
        except ValueError as e:
            # В случае ошибки API возвращаем 0 и логируем ошибку
            print(f"Error converting {currency} to RUB: {e}")
            return 0.0

    # Если неизвестная валюта - возвращаем 0
    return 0.0
