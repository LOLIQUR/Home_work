# Проект "Обработчик банковских транзакций"

## Описание
Проект предоставляет набор инструментов для обработки банковских операций.

## Установка
```bash
git clone https://github.com/LOLIQUR/Home_Work.git
cd Home_Work
poetry install
poetry shell
```

## Основные функции

### 1. Маскировка данных
```python
from src.masks import get_mask_card_number, get_mask_account

print(get_mask_card_number("1234567890123456"))  # "1234 56** **** 3456"
print(get_mask_account("40817810099910004312"))  # "**4312"
```

### 2. Обработка транзакций
```python
from src.processing import filter_by_state, sort_by_date

transactions = [
    {'id': 1, 'state': 'EXECUTED', 'date': '2023-01-01'},
    {'id': 2, 'state': 'CANCELED', 'date': '2023-01-02'}
]
filtered = filter_by_state(transactions, 'EXECUTED')
sorted_transactions = sort_by_date(transactions)
```

### 3. Форматирование
```python
from src.widget import mask_account_card, get_date

print(mask_account_card("Visa 1234567890123456"))  # "Visa 1234 56** **** 3456"
print(get_date("2023-01-01T12:00:00"))            # "01.01.2023"
```

## Новые модули

### Модуль utils
```python
import json

def load_transactions(file_path):
    """Загрузка транзакций из JSON-файла."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
```

### Модуль external_api
```python
import requests

def convert_to_ruble(transaction):
    """Конвертация валют в рубли с использованием внешнего API."""
    amount = float(transaction['operationAmount']['amount'])
    currency = transaction['operationAmount']['currency']['code']
    # Логика конвертации через API
    return amount * get_exchange_rate(currency)
```

## Модуль generators
```python
from src.generators import filter_by_currency, card_number_generator

usd_transactions = filter_by_currency(transactions, "USD")
for card in card_number_generator(1, 5):
    print(card)  # "0000 0000 0000 0001", ...
```

## Модуль decorators
```python
from src.decorators import log

@log(filename="log.txt")
def my_function(x, y):
    return x + y
```

## Тестирование
- Всего тестов: **49**
- Покрытие кода: **100%**
- Отчёт о покрытии: `htmlcov/index.html`

## Команда проекта
- Семенов Данил <mrjunkboy@vk.com>