# Проект "Обработчик банковских транзакций"

## Описание:
Проект предоставляет набор инструментов для обработки банковских операций, включая:
- Маскировку конфиденциальных данных (номера карт и счетов)
- Фильтрацию транзакций по статусу
- Сортировку операций по дате
- Форматирование финансовой информации

## Установка:

1. Клонируйте репозиторий:
```
git clone https://github.com/LOLIQUR/House_Work.git
cd House_Work
```
2. Установите зависимости через Poetry:
```
poetry install
```

3. Активируйте виртуальное окружение:
```
poetry shell
```

## Использование:

### Основные функции:

1. Маскировка данных
```
print(get_mask_card_number("1234567890123456"))  # "1234 56** **** 3456"
print(get_mask_account("40817810099910004312"))  # "**4312"
```

2. Обработка транзакций
```
transactions = [{'id': 1, 'state': 'EXECUTED', 'date': '2023-01-01'}]
filtered = filter_by_state(transactions)
sorted = sort_by_date(transactions)
```

3. Форматирование
```
print(mask_account_card("Visa 1234567890123456"))  # "Visa 1234 56** **** 3456"
print(get_date("2023-01-01T12:00:00"))  # "01.01.2023"
```

## Модуль generators

Модуль предоставляет генераторы для работы с банковскими транзакциями.

### Функции:

#### `filter_by_currency(transactions, currency)`
Фильтрует транзакции по заданной валюте и возвращает итератор.

```python
from src.generators import filter_by_currency

usd_transactions = filter_by_currency(transactions, "USD")
for transaction in usd_transactions:
    print(transaction["id"])
```

#### `transaction_descriptions(transactions)`
Генератор, который возвращает описания транзакций по очереди.

```python
from src.generators import transaction_descriptions

descriptions = transaction_descriptions(transactions)
for description in descriptions:
    print(description)
```

#### `card_number_generator(start, end)`
Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

```python
from src.generators import card_number_generator

for card_number in card_number_generator(1, 5):
    print(card_number)
# Вывод:
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# 0000 0000 0000 0003
# 0000 0000 0000 0004
# 0000 0000 0000 0005
```

## Модуль decorators

Модуль предоставляет декораторы для логирования работы функций.

### Декораторы:

#### `log(filename=None)`
Декоратор для автоматического логирования работы функций.

**Параметры:**
- `filename` (str, optional): Имя файла для записи логов. Если не указан, логи выводятся в консоль.

**Примеры использования:**

```python
from src.decorators import log

# Логирование в консоль
@log()
def add(a, b):
    return a + b

add(2, 3)  # Вывод в консоль: "add ok"

# Логирование в файл
@log(filename="operations.log")
def multiply(x, y):
    return x * y

multiply(4, 5)  # Запись в файл: "multiply ok"

# Логирование ошибок
@log()
def divide(a, b):
    return a / b

divide(10, 0)  # Вывод в консоль: "divide error: ZeroDivisionError. Inputs: (10, 0), {}"
```

**Формат логов:**
- При успешном выполнении: `"имя_функции ok"`
- При ошибке: `"имя_функции error: тип_ошибки. Inputs: (аргументы), {ключевые_аргументы}"`


## Команда проекта

- Семенов Данил <mrjunkboy@vk.com>