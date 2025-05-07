from datetime import datetime

from .masks import get_mask_account, get_mask_card_number  # Импорт из другого модуля


def mask_account_card(account_info: str) -> str:
    """
    Маскирует номер карты или счета в строке формата "Тип Номер".
    Использует импортированные функции для маскировки.

    """
    # Разделяем строку на тип и номер
    parts = account_info.rsplit(' ', 1)
    if len(parts) != 2:
        return account_info

    account_type, number = parts

    # Применяем соответствующую маскировку
    if account_type.lower() == 'счет':
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{account_type} {masked_number}"


def get_date(iso_date: str) -> str:
    """
    Преобразует дату в формат "ДД.ММ.ГГГГ".

    """
    try:
        dt = datetime.fromisoformat(iso_date)
        return dt.strftime("%d.%m.%Y")
    except ValueError as e:
        raise ValueError(f"Неверный формат даты: {iso_date}") from e

