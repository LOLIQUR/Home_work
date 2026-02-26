import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"code": "USD"}
            },
            "description": "Перевод организации"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"code": "USD"}
            },
            "description": "Перевод со счета на счет"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"code": "RUB"}
            },
            "description": "Перевод со счета на счет"
        }
    ]


class TestFilterByCurrency:
    """Тесты для функции filter_by_currency."""

    def test_filter_usd_transactions(self, sample_transactions):
        """Тестируем фильтрацию USD транзакций."""
        usd_transactions = list(filter_by_currency(sample_transactions, "USD"))
        assert len(usd_transactions) == 2
        assert all(t["operationAmount"]["currency"]["code"] == "USD" for t in usd_transactions)

    def test_filter_rub_transactions(self, sample_transactions):
        """Тестируем фильтрацию RUB транзакций."""
        rub_transactions = list(filter_by_currency(sample_transactions, "RUB"))
        assert len(rub_transactions) == 1
        assert rub_transactions[0]["id"] == 873106923

    def test_filter_empty_result(self, sample_transactions):
        """Тестируем фильтрацию несуществующей валюты."""
        eur_transactions = list(filter_by_currency(sample_transactions, "EUR"))
        assert len(eur_transactions) == 0


class TestTransactionDescriptions:
    """Тесты для генератора transaction_descriptions."""

    def test_descriptions_generator(self, sample_transactions):
        """Тестируем генератор описаний."""
        descriptions = list(transaction_descriptions(sample_transactions))
        expected = ["Перевод организации", "Перевод со счета на счет", "Перевод со счета на счет"]
        assert descriptions == expected


class TestCardNumberGenerator:
    """Тесты для генератора card_number_generator."""

    @pytest.mark.parametrize("start,end,expected_count", [
        (1, 5, 5),
        (10, 15, 6),
        (9999999999999995, 9999999999999999, 5)
    ])
    def test_card_number_range(self, start, end, expected_count):
        """Тестируем генерацию номеров в диапазоне."""
        cards = list(card_number_generator(start, end))
        assert len(cards) == expected_count

    def test_card_number_format(self):
        """Тестируем формат номеров карт."""
        cards = list(card_number_generator(1, 1))
        assert cards[0] == "0000 0000 0000 0001"

    def test_card_number_sequence(self):
        """Тестируем последовательность номеров."""
        cards = list(card_number_generator(1, 3))
        expected = ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]
        assert cards == expected
