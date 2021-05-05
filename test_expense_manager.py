import pytest
from Models.expense_manager import ExpenseManager

def test_attributes():
    """
    Tests if ExpenseManager class has the correct attributes and they are set correctly
    """
    manager = ExpenseManager()

    # Checks if private attribute exists
    assert hasattr(manager, "_expenses")

    # Checks if private attribute was set correctly
    assert manager._expenses == {}


def test_add_expense():
    """
    Tests for the add_expense method
    """
    manager = ExpenseManager()

    # Checks if method exists
    assert hasattr(manager, "add_expense")


def test_get_expenses():
    """
    Tests for the get_expenses method
    """
    manager = ExpenseManager()

    # Checks if method exists
    assert hasattr(manager, "get_expenses")

    # Checks if method returns correct value
    assert manager.get_expenses() == []


def test_from_csv():
    """
    Tests for the from_csv method
    """
    manager = ExpenseManager()

    # Checks if method exists
    assert hasattr(manager, "from_csv")


def test_to_csv():
    """
    Tests for the to_csv method
    """
    manager = ExpenseManager()

    # Checks if method exists
    assert hasattr(manager, "to_csv")


def test_read_largest_id():
    """
    Tests for the read_largest_id method
    """
    manager = ExpenseManager()

    # Checks if method exists
    assert hasattr(manager, "read_largest_id")
    