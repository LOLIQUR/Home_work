"""
Тесты для модуля file_processing.
"""
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.file_processing import read_csv, read_excel


class TestFileProcessing:
    """Тесты для функций чтения файлов."""

    @patch('pandas.read_csv')
    def test_read_csv_success(self, mock_read_csv):
        """Тест успешного чтения CSV."""
        # Создаём мок DataFrame
        mock_df = MagicMock()
        mock_df.to_dict.return_value = [
            {"id": 1, "amount": 100},
            {"id": 2, "amount": 200}
        ]
        mock_read_csv.return_value = mock_df

        result = read_csv("test.csv")

        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["amount"] == 200
        mock_read_csv.assert_called_once_with("test.csv")

    @patch('pandas.read_csv')
    def test_read_csv_error(self, mock_read_csv):
        """Тест ошибки при чтении CSV."""
        mock_read_csv.side_effect = Exception("File not found")

        result = read_csv("test.csv")

        assert result == []

    @patch('pandas.read_excel')
    def test_read_excel_success(self, mock_read_excel):
        """Тест успешного чтения Excel."""
        mock_df = MagicMock()
        mock_df.to_dict.return_value = [
            {"id": 1, "amount": 100},
            {"id": 2, "amount": 200}
        ]
        mock_read_excel.return_value = mock_df

        result = read_excel("test.xlsx")

        assert len(result) == 2
        assert result[0]["id"] == 1
        mock_read_excel.assert_called_once_with("test.xlsx")

    @patch('pandas.read_excel')
    def test_read_excel_error(self, mock_read_excel):
        """Тест ошибки при чтении Excel."""
        mock_read_excel.side_effect = Exception("File not found")

        result = read_excel("test.xlsx")

        assert result == []
