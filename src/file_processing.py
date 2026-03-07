"""
Модуль для чтения финансовых операций из CSV и Excel файлов.
"""
import pandas as pd
from typing import List, Dict, Any


def read_csv(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает транзакции из CSV файла.

    Args:
        file_path: Путь к CSV файлу

    Returns:
        Список словарей с транзакциями
    """
    try:
        df = pd.read_csv(file_path)
        return df.to_dict('records')
    except Exception as e:
        print(f"Ошибка при чтении CSV: {e}")
        return []


def read_excel(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает транзакции из Excel файла.

    Args:
        file_path: Путь к Excel файлу

    Returns:
        Список словарей с транзакциями
    """
    try:
        df = pd.read_excel(file_path)
        return df.to_dict('records')
    except Exception as e:
        print(f"Ошибка при чтении Excel: {e}")
        return []
