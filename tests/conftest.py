import pytest


@pytest.fixture
def sample_transactions():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01"},
        {"id": 2, "state": "CANCELED", "date": "2023-01-02"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-03"},
    ]
