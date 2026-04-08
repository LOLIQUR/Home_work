"""
Тесты для модуля views.
"""
import json
from unittest.mock import patch

from src.views import get_greeting, load_user_settings


class TestViews:
    """Тесты для функций views."""

    def test_get_greeting_morning(self):
        """Тест приветствия для утра."""
        with patch('src.views.datetime') as mock_datetime:
            mock_datetime.now.return_value.hour = 9
            assert get_greeting() == "Доброе утро"

    def test_get_greeting_day(self):
        """Тест приветствия для дня."""
        with patch('src.views.datetime') as mock_datetime:
            mock_datetime.now.return_value.hour = 14
            assert get_greeting() == "Добрый день"

    def test_get_greeting_evening(self):
        """Тест приветствия для вечера."""
        with patch('src.views.datetime') as mock_datetime:
            mock_datetime.now.return_value.hour = 20
            assert get_greeting() == "Добрый вечер"

    def test_get_greeting_night(self):
        """Тест приветствия для ночи."""
        with patch('src.views.datetime') as mock_datetime:
            mock_datetime.now.return_value.hour = 2
            assert get_greeting() == "Доброй ночи"

    def test_load_user_settings_success(self):
        """Тест загрузки настроек из файла."""
        mock_data = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(mock_data)
            result = load_user_settings()
            assert result == mock_data

    def test_load_user_settings_file_not_found(self):
        """Тест загрузки настроек при отсутствии файла."""
        with patch('builtins.open', side_effect=FileNotFoundError):
            result = load_user_settings()
            assert result == {"user_currencies": ["USD", "EUR"], "user_stocks": []}
