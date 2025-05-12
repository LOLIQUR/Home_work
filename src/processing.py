def filter_by_state(transactions: list[dict], state: str = 'EXECUTED') -> list[dict]:
    """
    Фильтрует транзакции по статусу ('EXECUTED' или 'CANCELED').

    Args:
        state: Статус транзакции. Только 'EXECUTED' или 'CANCELED'.
    """
    return [t for t in transactions if t.get('state') == state]


def sort_by_date(transactions: list[dict], reverse: bool = True) -> list[dict]:
    """
    Сортирует список словарей по дате.
    """
    return sorted(transactions, key=lambda x: x['date'], reverse=reverse)
