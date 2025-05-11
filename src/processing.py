def filter_by_state(transactions: list[dict], state: str = 'EXECUTED') -> list[dict]:
    """
    Фильтрует список словарей по значению ключа 'state'
    """
    return [t for t in transactions if t.get('state') == state]


def sort_by_date(transactions: list[dict], reverse: bool = True) -> list[dict]:
    """
    Сортирует список словарей по дате.
    """
    return sorted(transactions, key=lambda x: x['date'], reverse=reverse)