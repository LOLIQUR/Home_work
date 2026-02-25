"""
Модуль для работы с JSON-файлами и обработки транзакций.
"""
import json
from typing import List, Dict, Any


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из JSON-файла.

    Args:
        file_path: Путь к JSON-файлу

    Returns:
        Список словарей с транзакциями или пустой список в случае ошибки
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проверяем, что данные - список
        if isinstance(data, list):
            return data
        else:
            return []

    except (FileNotFoundError, json.JSONDecodeError, IOError):
        # Возвращаем пустой список при любой ошибке
        return []
