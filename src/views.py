"""
Модуль для генерации JSON-ответов для веб-страниц.
"""
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

# Настройка логгера
logger = logging.getLogger("views")
logger.setLevel(logging.DEBUG)
os.makedirs("logs", exist_ok=True)
file_handler = logging.FileHandler("logs/views.log", mode='w', encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)


def get_greeting() -> str:
    """Возвращает приветствие в зависимости от текущего времени."""
    hour = datetime.now().hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def load_user_settings() -> Dict[str, List[str]]:
    """Загружает настройки пользователя из файла user_settings.json."""
    try:
        with open("user_settings.json", "r", encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Ошибка загрузки настроек: {e}")
        return {"user_currencies": ["USD", "EUR"], "user_stocks": []}


def get_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    """Получает курсы валют к рублю через API."""
    rates = []
    for currency in currencies:
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{currency}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            rub_rate = data["rates"].get("RUB")
            if rub_rate:
                rates.append({"currency": currency, "rate": round(rub_rate, 2)})
                logger.info(f"Курс {currency}: {rub_rate} RUB")
        except Exception as e:
            logger.error(f"Ошибка получения курса {currency}: {e}")
            fallback = {"USD": 90.0, "EUR": 100.0}
            rates.append({"currency": currency, "rate": fallback.get(currency, 90.0)})
    return rates


def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """Получает цены акций (заглушка)."""
    mock_prices = {
        "AAPL": 175.12,
        "AMZN": 145.23,
        "GOOGL": 138.45,
        "MSFT": 420.56,
        "TSLA": 178.90
    }
    return [{"stock": stock, "price": mock_prices.get(stock, 100.0)} for stock in stocks]


def load_transactions_from_excel(file_path: str) -> pd.DataFrame:
    """Загружает транзакции из Excel-файла."""
    try:
        df = pd.read_excel(file_path)
        logger.info(f"Загружено {len(df)} транзакций из {file_path}")
        return df
    except Exception as e:
        logger.error(f"Ошибка загрузки Excel: {e}")
        return pd.DataFrame()


def get_card_data(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Анализирует траты по картам."""
    cards = {}
    for _, row in df.iterrows():
        card = str(row.get("Номер карты", ""))[-4:]
        if not card or card == 'nan':
            continue
        amount = float(row.get("Сумма операции", 0))
        if amount < 0:  # расходы (отрицательная сумма)
            spent = abs(amount)
            cards[card] = cards.get(card, {"spent": 0, "cashback": 0})
            cards[card]["spent"] += spent
            cards[card]["cashback"] += spent / 100
    return [
        {
            "last_digits": card,
            "total_spent": round(data["spent"], 2),
            "cashback": round(data["cashback"], 2)
        }
        for card, data in cards.items()
    ]


def get_top_transactions(df: pd.DataFrame, top_n: int = 5) -> List[Dict[str, Any]]:
    """Возвращает топ-N транзакций по сумме платежа."""
    df_filtered = df[df["Сумма операции"].notna()].copy()
    df_filtered = df_filtered.sort_values("Сумма операции", ascending=False)
    top = []
    for _, row in df_filtered.head(top_n).iterrows():
        top.append({
            "date": str(row.get("Дата операции", ""))[:10],
            "amount": round(float(row.get("Сумма операции", 0)), 2),
            "category": str(row.get("Категория", "")),
            "description": str(row.get("Описание", ""))[:50]
        })
    return top


def main_page(date_str: str) -> str:
    """
    Главная функция для страницы "Главная".

    Args:
        date_str: Дата и время в формате "YYYY-MM-DD HH:MM:SS"

    Returns:
        JSON-строка с данными для веб-страницы
    """
    logger.info(f"Запрос главной страницы на дату: {date_str}")

    df = load_transactions_from_excel("data/operations.xlsx")
    settings = load_user_settings()
    currencies = settings.get("user_currencies", ["USD", "EUR"])
    stocks = settings.get("user_stocks", [])

    result = {
        "greeting": get_greeting(),
        "cards": get_card_data(df),
        "top_transactions": get_top_transactions(df, 5),
        "currency_rates": get_currency_rates(currencies),
        "stock_prices": get_stock_prices(stocks)
    }

    logger.info("Главная страница успешно сформирована")
    return json.dumps(result, ensure_ascii=False, indent=2)
