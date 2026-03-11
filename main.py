"""
Главный модуль программы с пользовательским интерфейсом.
"""
import json
from src.file_processing import read_csv, read_excel
from src.utils import load_transactions
from src.search import filter_by_description
from src.processing import filter_by_state, sort_by_date
from src.widget import mask_account_card, get_date


def main():
    """Основная логика программы."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("> ").strip()

    # Загрузка данных
    if choice == "1":
        print("Для обработки выбран JSON-файл.")
        transactions = load_transactions("data/operations.json")
    elif choice == "2":
        print("Для обработки выбран CSV-файл.")
        transactions = read_csv("data/transactions.csv")
    elif choice == "3":
        print("Для обработки выбран XLSX-файл.")
        transactions = read_excel("data/transactions_excel.xlsx")
    else:
        print("Неверный выбор. Загружаем JSON по умолчанию.")
        transactions = load_transactions("data/operations.json")

    if not transactions:
        print("Не удалось загрузить транзакции.")
        return

    # Фильтрация по статусу
    valid_statuses = {"EXECUTED", "CANCELED", "PENDING"}
    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        status = input("> ").strip().upper()

        if status in valid_statuses:
            transactions = filter_by_state(transactions, status)
            print(f"Операции отфильтрованы по статусу \"{status}\"")
            break
        else:
            print(f"Статус операции \"{status}\" недоступен.")

    # Сортировка по дате
    sort_choice = input("\nОтсортировать операции по дате? Да/Нет\n> ").strip().lower()
    if sort_choice in ["да", "yes", "y", "д"]:
        order = input("Отсортировать по возрастанию или по убыванию?\n> ").strip().lower()
        reverse = order in ["убывание", "убыванию", "desc", "по убыванию"]
        transactions = sort_by_date(transactions, reverse)

    # Фильтрация по рублям
    rub_choice = input("\nВыводить только рублевые транзакции? Да/Нет\n> ").strip().lower()
    if rub_choice in ["да", "yes", "y", "д"]:
        transactions = [t for t in transactions if
                        t.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"]

    # Фильтрация по описанию
    desc_choice = input(
        "\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет\n> ").strip().lower()
    if desc_choice in ["да", "yes", "y", "д"]:
        word = input("Введите слово для поиска:\n> ").strip()
        transactions = filter_by_description(transactions, word)

    # Вывод результатов
    print("\nРаспечатываю итоговый список транзакций...\n")

    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Всего банковских операций в выборке: {len(transactions)}\n")

    for t in transactions:
        date = get_date(t.get("date", ""))
        desc = t.get("description", "")

        # Форматирование счёта/карты
        if "from" in t and "to" in t:
            from_masked = mask_account_card(t["from"]) if t["from"] else "Неизвестно"
            to_masked = mask_account_card(t["to"])
            print(f"{date} {desc}\n{from_masked} -> {to_masked}")
        elif "to" in t:
            to_masked = mask_account_card(t["to"])
            print(f"{date} {desc}\n{to_masked}")
        else:
            print(f"{date} {desc}")

        # Сумма и валюта
        amount = t.get("operationAmount", {}).get("amount", "0")
        currency = t.get("operationAmount", {}).get("currency", {}).get("code", "RUB")
        print(f"Сумма: {amount} {currency}\n")


if __name__ == "__main__":
    main()
