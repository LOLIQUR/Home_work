"""
Модуль для отчётов: траты по категориям, дням недели и т.д.
"""
import json
import logging
import os
from datetime import datetime, timedelta
from functools import wraps
from typing import Optional

import pandas as pd

# Настройка логгера
logger = logging.getLogger("reports")
logger.setLevel(logging.DEBUG)
os.makedirs("logs", exist_ok=True)
file_handler = logging.FileHandler("logs/reports.log", mode='w', encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)


def save_to_file(filename: str = None):
    """
    Декоратор для сохранения результата отчёта в файл.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            output_filename = filename or f"report_{func.__name__}.json"
            try:
                with open(output_filename, 'w', encoding='utf-8') as f:
                    if isinstance(result, dict):
                        f.write(json.dumps(result, ensure_ascii=False, indent=2))
                    else:
                        f.write(str(result))
                logger.info(f"Отчёт сохранён в {output_filename}")
            except Exception as e:
                logger.error(f"Ошибка сохранения отчёта: {e}")
            return result

        return wrapper

    return decorator


def load_transactions_from_excel(file_path: str) -> pd.DataFrame:
    """Загружает транзакции из Excel."""
    try:
        df = pd.read_excel(file_path)
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
        logger.info(f"Загружено {len(df)} транзакций")
        return df
    except Exception as e:
        logger.error(f"Ошибка загрузки Excel: {e}")
        return pd.DataFrame()


@save_to_file()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> dict:
    """
    Отчёт: траты по заданной категории за последние 3 месяца.

    Args:
        transactions: DataFrame с транзакциями
        category: Название категории
        date: Опциональная дата (формат "YYYY-MM-DD")

    Returns:
        Словарь с тратами по дням
    """
    if date:
        end_date = pd.to_datetime(date)
    else:
        end_date = datetime.now()

    start_date = end_date - timedelta(days=90)

    logger.info(f"Отчёт по категории '{category}' за период {start_date.date()} - {end_date.date()}")

    # Фильтруем по дате и категории
    mask = (transactions["Дата операции"] >= start_date) & (transactions["Дата операции"] <= end_date)
    filtered = transactions[mask]

    # Только расходы (отрицательная сумма) по нужной категории
    expenses = filtered[(filtered["Сумма операции"] < 0) & (filtered["Категория"] == category)]

    # Группируем по дате
    daily_expenses = expenses.groupby(expenses["Дата операции"].dt.date)["Сумма операции"].sum().abs()

    result = {
        "category": category,
        "period": {
            "from": start_date.strftime("%Y-%m-%d"),
            "to": end_date.strftime("%Y-%m-%d")
        },
        "total_spent": round(daily_expenses.sum(), 2),
        "days_count": len(daily_expenses),
        "daily_breakdown": {str(k): round(v, 2) for k, v in daily_expenses.items()}
    }

    logger.info(f"Всего потрачено: {result['total_spent']} руб.")
    return result
