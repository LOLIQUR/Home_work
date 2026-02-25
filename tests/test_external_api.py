"""
Тесты для модуля external_api.
"""
import pytest
from unittest.mock import patch, MagicMock
from src.external_api import convert_to_ruble, get_exchange_rate


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

    @patch('src.external_api.get_exchange_rate')
    def test_convert_eur_transaction_success(self, mock_get_rate):
        """Тест успешной конвертации EUR транзакции с Mock."""
        mock_get_rate.return_value = 100.5

        transaction = {
            "operationAmount": {
                "amount": "50.00",
                "currency": {"code": "EUR"}
            }
        }
        result = convert_to_ruble(transaction)

        assert result == 50.00 * 100.5
        mock_get_rate.assert_called_once_with("EUR")

    @patch('src.external_api.get_exchange_rate')
    def test_convert_usd_transaction_with_fallback(self, mock_get_rate):
        """Тест использования запасного курса при ошибке API."""
        mock_get_rate.side_effect = ValueError("API error")

        transaction = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": "USD"}
            }
        }
        result = convert_to_ruble(transaction)

        # Должен использовать запасной курс 90.0
        assert result == 100.00 * 90.0

    @patch('src.external_api.get_exchange_rate')
    def test_convert_usd_transaction_success(self, mock_get_rate):
        """Тест успешной конвертации USD транзакции с Mock."""
        mock_get_rate.return_value = 90.5

        transaction = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": "USD"}
            }
        }
        result = convert_to_ruble(transaction)

        assert result == 100.00 * 90.5
        mock_get_rate.assert_called_once_with("USD")

    @patch('src.external_api.requests.get')
    def test_get_exchange_rate_success(self, mock_get):
        """Тест успешного получения курса валют через API."""
        # Создаём мок-ответ
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "rates": {"RUB": 92.3}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Вызываем функцию
        rate = get_exchange_rate("USD")

        # Проверяем результаты
        assert rate == 92.3
        mock_get.assert_called_once_with("https://api.exchangerate-api.com/v4/latest/USD")

    @patch('src.external_api.requests.get')
    def test_get_exchange_rate_error(self, mock_get):
        """Тест обработки ошибки API."""
        mock_get.side_effect = Exception("Connection error")

        with pytest.raises(ValueError, match="Failed to fetch exchange rate"):
            get_exchange_rate("USD")

    def test_convert_unknown_currency(self):
        """Тест конвертации неизвестной валюты."""
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

    @patch('src.external_api.requests.get')
    def test_get_exchange_rate_no_rub_rate(self, mock_get):
        """Тест обработки отсутствия курса RUB в ответе API (строка 33)."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "rates": {}  # Пустой словарь, нет RUB
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="RUB rate not found"):
            get_exchange_rate("USD")

    @patch('src.external_api.requests.get')
    def test_get_exchange_rate_request_exception(self, mock_get):
        """Тест обработки RequestException (строка 39)."""
        from requests.exceptions import RequestException
        mock_get.side_effect = RequestException("Connection failed")

        with pytest.raises(ValueError, match="Failed to fetch exchange rate"):
            get_exchange_rate("USD")
