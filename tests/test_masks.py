import pytest
from src.masks import get_mask_card_number, get_mask_account


@pytest.mark.parametrize("card_num, expected", [
    ("1234567890123456", "1234 56** **** 3456"),
    ("123456789012", "1234 56** **** 9012"),
    ("", ""),
])
def test_get_mask_card_number(card_num, expected):
    assert get_mask_card_number(card_num) == expected


@pytest.mark.parametrize("account, expected", [
    ("40817810099910004312", "**4312"),
    ("1234", "**1234"),
    ("", ""),
])
def test_get_mask_account(account, expected):
    assert get_mask_account(account) == expected
