"""
Тесты для модуля external_api.
"""
import pytest
from unittest.mock import patch, MagicMock
from src.external_api import convert_to_ruble


class TestExternalAPI:
    """Тесты для модуля external_api."""

    def test_convert_rub_transaction(self):
        """Тест конвертации RUB транзакции (должна вернуть ту же сумму)."""
        transaction = {
            "operationAmount": {
                "amount": "1000.50",
                "currency": {"code": "RUB"}
            }
        }
        result = convert_to_ruble(transaction)
        assert result == 1000.50
        assert isinstance(result, float)

    def test_convert_unknown_currency(self):
        """Тест конвертации неизвестной валюты (должен вернуть 0)."""
        transaction = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": "GBP"}
            }
        }
        result = convert_to_ruble(transaction)
        assert result == 0.0

    def test_transaction_without_amount(self):
        """Тест транзакции без суммы."""
        transaction = {
            "operationAmount": {
                "currency": {"code": "USD"}
            }
        }
        result = convert_to_ruble(transaction)
        assert result == 0.0

    def test_transaction_without_operation_amount(self):
        """Тест транзакции без поля operationAmount."""
        transaction = {}
        result = convert_to_ruble(transaction)
        assert result == 0.0

    @patch('src.external_api.os.getenv')
    def test_missing_api_key(self, mock_getenv):
        """Тест отсутствия API ключа."""
        mock_getenv.return_value = None

        transaction = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": "USD"}
            }
        }

        with pytest.raises(ValueError, match="API key not found"):
            convert_to_ruble(transaction)

    @patch('src.external_api.requests.get')
    @patch('src.external_api.os.getenv')
    def test_convert_usd_success(self, mock_getenv, mock_get):
        """Тест успешной конвертации USD через API."""
        # Настраиваем моки
        mock_getenv.return_value = "fake_api_key"

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            "result": 9000.0  # 100 USD * 90 RUB
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        transaction = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": "USD"}
            }
        }

        result = convert_to_ruble(transaction)

        # Проверяем результат
        assert result == 9000.0

        # Проверяем что запрос был сделан правильно
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert args[0] == "https://api.apilayer.com/exchangerates_data/convert"
        assert kwargs["params"] == {"to": "RUB", "from": "USD", "amount": 100.0}
        assert kwargs["headers"] == {"apikey": "fake_api_key"}

    @patch('src.external_api.requests.get')
    @patch('src.external_api.os.getenv')
    def test_convert_eur_success(self, mock_getenv, mock_get):
        """Тест успешной конвертации EUR через API."""
        mock_getenv.return_value = "fake_api_key"

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            "result": 5000.0  # 50 EUR * 100 RUB
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        transaction = {
            "operationAmount": {
                "amount": "50.00",
                "currency": {"code": "EUR"}
            }
        }

        result = convert_to_ruble(transaction)
        assert result == 5000.0

    @patch('src.external_api.requests.get')
    @patch('src.external_api.os.getenv')
    def test_api_error_response(self, mock_getenv, mock_get):
        """Тест обработки ошибки от API."""
        mock_getenv.return_value = "fake_api_key"

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": False,
            "error": {
                "info": "Invalid API key"
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        transaction = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": "USD"}
            }
        }

        result = convert_to_ruble(transaction)
        assert result == 0.0

    @patch('src.external_api.requests.get')
    @patch('src.external_api.os.getenv')
    def test_network_error(self, mock_getenv, mock_get):
        """Тест обработки сетевой ошибки."""
        mock_getenv.return_value = "fake_api_key"
        mock_get.side_effect = Exception("Network error")

        transaction = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": "USD"}
            }
        }

        result = convert_to_ruble(transaction)
        assert result == 0.0
