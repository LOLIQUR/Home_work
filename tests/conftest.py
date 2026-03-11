import pytest


@pytest.fixture
def sample_transactions():
    """Фикстура с транзакциями, содержащими description."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01", "description": "Перевод организации"},
        {"id": 2, "state": "CANCELED", "date": "2023-01-02", "description": "Перевод с карты на карту"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-03", "description": "Открытие вклада"},
        {"id": 4, "state": "EXECUTED", "date": "2023-01-04", "description": "Перевод со счета на счет"},
    ]
