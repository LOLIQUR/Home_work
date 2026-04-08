"""
Тесты для модуля reports.
"""
from unittest.mock import MagicMock, patch

import pandas as pd

from src.reports import load_transactions_from_excel, spending_by_category


class TestReports:
    """Тесты для отчётов."""

    @patch('src.reports.pd.read_excel')
    def test_load_transactions_from_excel_success(self, mock_read_excel):
        """Тест успешной загрузки Excel."""
        mock_df = MagicMock()
        mock_read_excel.return_value = mock_df
        result = load_transactions_from_excel("test.xlsx")
        assert result is not None

    def test_spending_by_category(self):
        """Тест отчёта по категории."""
        data = {
            "Дата операции": ["2024-01-01", "2024-01-15", "2024-02-01", "2024-03-01"],
            "Категория": ["Супермаркеты", "Супермаркеты", "Переводы", "Супермаркеты"],
            "Сумма операции": [-100, -200, -50, -150]
        }
        df = pd.DataFrame(data)
        df["Дата операции"] = pd.to_datetime(df["Дата операции"])

        result = spending_by_category(df, "Супермаркеты", "2024-03-31")
        assert result["category"] == "Супермаркеты"
        assert result["total_spent"] == 450.0
        assert result["days_count"] == 3
