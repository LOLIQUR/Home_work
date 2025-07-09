import pytest
from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_transactions():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01"},
        {"id": 2, "state": "CANCELED", "date": "2023-01-02"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-03"},
    ]

@pytest.mark.parametrize("state, expected_ids", [
    ("EXECUTED", [1, 3]),
    ("CANCELED", [2]),
    ("PENDING", []),
])
def test_filter_by_state(sample_transactions, state, expected_ids):
    result = filter_by_state(sample_transactions, state)
    assert [t["id"] for t in result] == expected_ids