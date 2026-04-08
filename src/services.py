"""
Модуль для сервисов: простой поиск, инвестиции, кешбэк и т.д.
"""
import json
import logging
import os
from typing import List, Dict, Any
import pandas as pd

# Настройка логгера
logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
os.makedirs("logs", exist_ok=True)
file_handler = logging.FileHandler("logs/services.log", mode='w', encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)


def simple_search(transactions: List[Dict[str, Any]], query: str) -> str:
    """
    Сервис простого поиска.
    Ищет транзакции, содержащие query в описании или категории.

    Args:
        transactions: Список словарей с транзакциями
        query: Строка для поиска

    Returns:
        JSON-строка с найденными транзакциями
    """
    logger.info(f"Поиск транзакций по запросу: '{query}'")

    if not query:
        logger.warning("Пустой поисковый запрос")
        return json.dumps([], ensure_ascii=False, indent=2)

    query_lower = query.lower()
    result = []

    for t in transactions:
        description = str(t.get("Описание", "")).lower()
        category = str(t.get("Категория", "")).lower()

        if query_lower in description or query_lower in category:
            result.append({
                "date": t.get("Дата операции", ""),
                "amount": float(t.get("Сумма операции", 0)),
                "currency": t.get("Валюта операции", "RUB"),
                "category": t.get("Категория", ""),
                "description": t.get("Описание", "")
            })

    logger.info(f"Найдено {len(result)} транзакций")
    return json.dumps(result, ensure_ascii=False, indent=2)


def load_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из Excel и возвращает список словарей."""
    try:
        df = pd.read_excel(file_path)
        logger.info(f"Загружено {len(df)} транзакций")
        return df.to_dict('records')
    except Exception as e:
        logger.error(f"Ошибка загрузки Excel: {e}")
        return []
