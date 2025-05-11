def filter_by_state(transactions: list[dict], state: str = 'EXECUTED') -> list[dict]:
    """
    Фильтрует список словарей по значению ключа 'state'
    """
    return [t for t in transactions if t.get('state') == state]