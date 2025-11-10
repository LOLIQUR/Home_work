def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты, оставляя первые 6 и последние 4 цифры.
    Всегда возвращает 4 группы по 4 цифры, добавляя **** при необходимости.
    """
    digits_only = ''.join(c for c in card_number if c.isdigit())

    if len(digits_only) < 10:
        return '*' * len(digits_only)

    first_six = digits_only[:6]
    last_four = digits_only[-4:]

    # Всегда выводим 4 группы по 4 цифры
    return f"{first_six[:4]} {first_six[4:6]}** **** {last_four}"


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счёта, оставляя только последние 4 цифры,
    перед ними ставит две звёздочки.

    Пример:
        40817810099910004312 → **4312
    """
    digits_only = ''.join(c for c in account_number if c.isdigit())

    if len(digits_only) < 4:
        return '*' * len(digits_only)

    return '**' + digits_only[-4:]
