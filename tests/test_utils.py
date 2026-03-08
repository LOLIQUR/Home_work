"""
Тесты для модуля utils.
"""

from unittest.mock import mock_open, patch

from src.utils import load_transactions


class TestUtils:
    """Тесты для модуля utils."""

    @patch('builtins.open', new_callable=mock_open, read_data='[{"id": 1, "amount": 100}]')
    def test_load_transactions_success(self, mock_file):
        """Тест успешной загрузки транзакций из JSON."""
        result = load_transactions("dummy_path.json")

        assert len(result) == 1
        assert result[0]["id"] == 1
        assert result[0]["amount"] == 100
        mock_file.assert_called_once_with("dummy_path.json", 'r', encoding='utf-8')

    @patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
    def test_load_transactions_not_list(self, mock_file):
        """Тест загрузки, когда JSON не является списком."""
        result = load_transactions("dummy_path.json")

        assert result == []

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_transactions_file_not_found(self, mock_file):
        """Тест обработки отсутствующего файла."""
        result = load_transactions("nonexistent.json")

        assert result == []

    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    def test_load_transactions_invalid_json(self, mock_file):
        """Тест обработки некорректного JSON."""
        result = load_transactions("dummy_path.json")

        assert result == []

    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_load_transactions_empty_list(self, mock_file):
        """Тест загрузки пустого списка."""
        result = load_transactions("dummy_path.json")

        assert result == []
