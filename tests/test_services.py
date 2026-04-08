"""
Тесты для модуля services.
"""
import json

from src.services import simple_search


class TestServices:
    """Тесты для сервисов."""

    def test_simple_search_found(self):
        """Тест поиска существующей транзакции."""
        transactions = [
            {"Описание": "Перевод Константин Л.", "Категория": "Переводы", "Дата операции": "2024-01-01",
             "Сумма операции": -100, "Валюта операции": "RUB"},
            {"Описание": "Покупка в магазине", "Категория": "Супермаркеты", "Дата операции": "2024-01-02",
             "Сумма операции": -500, "Валюта операции": "RUB"}
        ]
        result = simple_search(transactions, "Константин")
        data = json.loads(result)
        assert len(data) == 1
        assert data[0]["description"] == "Перевод Константин Л."

    def test_simple_search_not_found(self):
        """Тест поиска отсутствующей транзакции."""
        transactions = [{"Описание": "Перевод", "Категория": "Переводы"}]
        result = simple_search(transactions, "несуществующее")
        data = json.loads(result)
        assert len(data) == 0

    def test_simple_search_empty_query(self):
        """Тест поиска с пустым запросом."""
        transactions = [{"Описание": "Перевод"}]
        result = simple_search(transactions, "")
        data = json.loads(result)
        assert len(data) == 0

    def test_simple_search_empty_list(self):
        """Тест поиска в пустом списке."""
        result = simple_search([], "перевод")
        data = json.loads(result)
        assert len(data) == 0
