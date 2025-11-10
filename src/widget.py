from datetime import datetime

from .masks import get_mask_account, get_mask_card_number  # Импорт из другого модуля


def mask_account_card(account_info: str) -> str:
    """Маскирует номер карты или счета в строке формата 'Тип номер'."""
    parts = account_info.rsplit(' ', maxsplit=1)
    if len(parts) != 2:
        return account_info

    account_type, number = parts

    if account_type.lower() == "счет":
        masked_number = get_mask_account(number)
    elif any(word in account_type.lower() for word in ["visa", "mastercard", "мир"]):
        masked_number = get_mask_card_number(number)
    else:
        return account_info  # Не маскируем неизвестные форматы

    return f"{account_type} {masked_number}"


def get_date(iso_date: str) -> str:
    """
    Преобразует дату в формат "ДД.ММ.ГГГГ".
    """
    if not iso_date:
        return ""
    return datetime.fromisoformat(iso_date).strftime('%d.%m.%Y')
