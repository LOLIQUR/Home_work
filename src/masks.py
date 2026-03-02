"""
Модуль для маскировки банковских карт и счетов.
"""
import logging
import os
from typing import Union

# Настройка логгера для модуля masks
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

# Создаём папку logs если её нет
os.makedirs("logs", exist_ok=True)

# Настройка файлового обработчика
file_handler = logging.FileHandler("logs/masks.log", mode='w', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# Настройка форматтера
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(file_handler)


def get_mask_card_number(card_number: Union[str, int]) -> str:
    """
    Маскирует номер банковской карты.

    Args:
        card_number: Номер карты (строка или число)

    Returns:
        Замаскированный номер карты
    """
    logger.info(f"Начало маскирования карты: {str(card_number)[:4]}****...")

    try:
        # Преобразуем в строку и удаляем всё кроме цифр
        card_str = str(card_number)
        digits_only = ''.join(filter(str.isdigit, card_str))

        if len(digits_only) < 10:
            logger.error(f"Недостаточно цифр в номере карты: {len(digits_only)}")
            return "**** **** **** ****"

        # Маскируем: первые 6 и последние 4 цифры
        first_six = digits_only[:6]
        last_four = digits_only[-4:]

        # Форматируем с маской
        result = f"{first_six[:4]} {first_six[4:6]}** **** {last_four}"

        logger.info(f"Карта успешно замаскирована")
        return result

    except Exception as e:
        logger.error(f"Ошибка при маскировании карты: {e}", exc_info=True)
        return "**** **** **** ****"


def get_mask_account(account_number: Union[str, int]) -> str:
    """
    Маскирует номер банковского счёта.

    Args:
        account_number: Номер счёта (строка или число)

    Returns:
        Замаскированный номер счёта
    """
    logger.info(f"Начало маскирования счёта")

    try:
        # Преобразуем в строку и удаляем всё кроме цифр
        account_str = str(account_number)
        digits_only = ''.join(filter(str.isdigit, account_str))

        if len(digits_only) < 4:
            logger.error(f"Недостаточно цифр в номере счёта: {len(digits_only)}")
            return "****"

        # Оставляем только последние 4 цифры
        last_four = digits_only[-4:]
        result = f"**{last_four}"

        logger.info(f"Счёт успешно замаскирован")
        return result

    except Exception as e:
        logger.error(f"Ошибка при маскировании счёта: {e}", exc_info=True)
        return "****"
