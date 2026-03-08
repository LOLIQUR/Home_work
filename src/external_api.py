"""
Модуль для работы с внешним API конвертации валют (apilayer.com).
"""
import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()


def convert_to_ruble(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли, используя API apilayer.

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
    if currency not in ["USD", "EUR"]:
        return 0.0

    # Получаем API-ключ из переменных окружения
    api_key = os.getenv("EXCHANGE_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Check your .env file.")

    # Формируем запрос к API apilayer (эндпоинт convert)
    url = "https://api.apilayer.com/exchangerates_data/convert"

    params = {
        "to": "RUB",
        "from": currency,
        "amount": amount
    }

    headers = {
        "apikey": api_key  # Ключ передается в заголовке
    }

    try:
        # Отправляем запрос
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Проверяем успешность запроса
        if not data.get("success"):
            error_info = data.get('error', {}).get('info', 'Unknown API error')
            print(f"API error: {error_info}")
            return 0.0

        return float(data["result"])

    except Exception as e:
        # ЛОВИМ ВСЕ исключения!
        print(f"Error during currency conversion: {type(e).__name__}: {e}")
        return 0.0
