def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты, оставляя первые 6 и последние 4 цифры.
    Остальные заменяются на '*'.

    Пример:
        1234567890123456 → 1234 56** **** 3456
    """
    digits_only = ''.join(c for c in card_number if c.isdigit())

    if len(digits_only) < 10:
        return '*' * len(digits_only)

    first_six = digits_only[:6]
    last_four = digits_only[-4:]
    masked_middle = '*' * (len(digits_only) - 10)
    grouped = first_six + masked_middle + last_four

    # Разбиваем по 4 цифры
    return ' '.join(grouped[i:i + 4] for i in range(0, len(grouped), 4))


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
