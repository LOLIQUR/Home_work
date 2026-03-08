"""
Модуль для работы с JSON-файлами и обработки транзакций.
"""
import json
import logging
import os
from typing import Any, Dict, List

# Настройка логгера для модуля utils
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

# Создаём папку logs если её нет
os.makedirs("logs", exist_ok=True)

# Настройка файлового обработчика
file_handler = logging.FileHandler("logs/utils.log", mode='w', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# Настройка форматтера
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(file_handler)


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из JSON-файла.

    Args:
        file_path: Путь к JSON-файлу

    Returns:
        Список словарей с транзакциями или пустой список в случае ошибки
    """
    logger.info(f"Попытка загрузки файла: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проверяем, что данные - список
        if isinstance(data, list):
            logger.info(f"Успешно загружено {len(data)} транзакций")
            return data
        else:
            logger.error(f"Файл содержит не список, а {type(data).__name__}")
            return []

    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON: {e}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}", exc_info=True)
        return []
