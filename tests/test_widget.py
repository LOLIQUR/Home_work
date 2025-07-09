import pytest
from src.widget import mask_account_card, get_date


@pytest.mark.parametrize("input_str, expected", [
    ("Visa 1234567890123456", "Visa 1234 56** **** 3456"),
    ("Счет 40817810099910004312", "Счет **4312"),
    ("Неизвестный 123456", "Неизвестный 123456")  # Неподдерживаемый формат
])
def test_mask_account_card(input_str, expected):
    assert mask_account_card(input_str) == expected


@pytest.mark.parametrize("iso_date, expected", [
    ("2023-01-01T12:00:00", "01.01.2023"),
    ("2022-12-31T23:59:59", "31.12.2022"),
    ("", "")  # Пустая строка
])
def test_get_date(iso_date, expected):
    assert get_date(iso_date) == expected