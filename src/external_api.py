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
    # Используем бесплатный API без ключа
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        rub_rate = data["rates"].get("RUB")
        if not rub_rate:
            raise ValueError(f"RUB rate not found for {base_currency}")

        return rub_rate

    except requests.RequestException as e:
        # Преобразуем RequestException в ValueError
        raise ValueError(f"Failed to fetch exchange rate: {str(e)}")
    except Exception as e:
        # Любые другие ошибки тоже преобразуем в ValueError
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
            # В случае ошибки API используем запасной курс
            print(f"Warning: Using fallback rate for {currency}: {e}")
            fallback_rates = {"USD": 90.0, "EUR": 100.0}
            return amount * fallback_rates.get(currency, 90.0)

    # Если неизвестная валюта - возвращаем 0
    return 0.0
