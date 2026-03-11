"""
Тесты для модуля search.
"""

from src.search import count_by_categories, filter_by_description


class TestSearch:
    """Тесты для функций поиска и подсчёта."""

    def test_filter_by_description_found(self, sample_transactions):
        """Тест поиска существующего описания."""
        result = filter_by_description(sample_transactions, "перевод")
        assert len(result) == 3
        assert all("перевод" in t["description"].lower() for t in result)

    def test_filter_by_description_not_found(self, sample_transactions):
        """Тест поиска отсутствующего описания."""
        result = filter_by_description(sample_transactions, "несуществующее")
        assert result == []

    def test_filter_by_description_empty(self):
        """Тест поиска в пустом списке."""
        result = filter_by_description([], "перевод")
        assert result == []

    def test_filter_by_description_case_insensitive(self, sample_transactions):
        """Тест регистронезависимого поиска."""
        result_lower = filter_by_description(sample_transactions, "перевод")
        result_upper = filter_by_description(sample_transactions, "ПЕРЕВОД")
        assert len(result_lower) == len(result_upper)

    def test_count_by_categories(self, sample_transactions):
        """Тест подсчёта по категориям."""
        categories = ["перевод", "вклад", "карта"]
        result = count_by_categories(sample_transactions, categories)

        assert isinstance(result, dict)
        assert result.get("перевод", 0) > 0
        assert "вклад" in result
        assert "карта" in result

    def test_count_by_categories_empty(self):
        """Тест подсчёта в пустом списке."""
        result = count_by_categories([], ["перевод"])
        assert result == {"перевод": 0}
