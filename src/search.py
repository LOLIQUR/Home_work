"""
Модуль для поиска и подсчёта банковских операций.
"""
import re
from collections import Counter
from typing import Any, Dict, List


def filter_by_description(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по наличию строки в описании.

    Args:
        transactions: Список транзакций
        search_string: Строка для поиска

    Returns:
        Список транзакций, в описании которых есть искомая строка
    """
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    return [t for t in transactions if pattern.search(t.get("description", ""))]


def count_by_categories(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество транзакций по заданным категориям.

    Args:
        transactions: Список транзакций
        categories: Список категорий для подсчёта

    Returns:
        Словарь с количеством транзакций по каждой категории
    """
    descriptions = [t.get("description", "") for t in transactions]
    counter = Counter()

    for category in categories:
        pattern = re.compile(re.escape(category), re.IGNORECASE)
        count = sum(1 for desc in descriptions if pattern.search(desc))
        counter[category] = count

    return dict(counter)
