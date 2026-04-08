import json
from src.services import load_transactions_from_excel, simple_search

# Загружаем данные
transactions = load_transactions_from_excel("data/operations.xlsx")
print(f"Загружено транзакций: {len(transactions)}")

# Ищем по слову "перевод"
result = simple_search(transactions, "перевод")
print("\nРезультат поиска 'перевод':")
print(result[:800])  # первые 800 символов

# Ищем по слову "супермаркет"
result2 = simple_search(transactions, "супермаркет")
print(f"\nНайдено по 'супермаркет': {len(json.loads(result2))} шт.")

# Ищем по слову "кафе"
result3 = simple_search(transactions, "кафе")
print(f"Найдено по 'кафе': {len(json.loads(result3))} шт.")
