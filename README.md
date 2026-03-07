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

## Модуль file_processing

Модуль для чтения финансовых операций из CSV и Excel файлов.

### Функции

#### `read_csv(file_path: str) -> List[Dict[str, Any]]`
Читает транзакции из CSV файла.

**Параметры:**
- `file_path` — путь к CSV файлу

**Возвращает:**
- Список словарей с транзакциями

**Пример:**
```python
from src.file_processing import read_csv

transactions = read_csv('data/transactions.csv')
print(f'Загружено {len(transactions)} транзакций')
```

#### `read_excel(file_path: str) -> List[Dict[str, Any]]`
Читает транзакции из Excel файла.

**Параметры:**
- `file_path` — путь к Excel файлу

**Возвращает:**
- Список словарей с транзакциями

**Пример:**
```python
from src.file_processing import read_excel

transactions = read_excel('data/transactions_excel.xlsx')
print(f'Загружено {len(transactions)} транзакций')
```

### Зависимости
- `pandas` — для чтения CSV и Excel
- `openpyxl` — для работы с Excel файлами

### Тестирование
- 4 теста с использованием Mock и patch
- 100% покрытие кода

## Команда проекта

- Семенов Данил <mrjunkboy@vk.com>
