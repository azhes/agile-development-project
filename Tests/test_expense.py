import pytest
from Models.expense import Expense
from datetime import date
from datetime import datetime

def test_attributes():
    """
    Tests if Expense class has the correct attributes and they are set correctly
    """
    expense = Expense(1, "school", 200)

    # Checks if private attributes exist
    assert hasattr(expense, "_ID")
    assert hasattr(expense, "_Category")
    assert hasattr(expense, "_Amount")
    assert hasattr(expense, "_Date")

    # Checks private attributes were assigned correctly
    assert expense._ID == 1
    assert expense._Category == "school"
    assert expense._Amount == "200.00"
    assert expense._Date == date.today()


def test_properties():
    """
    Tests for Expense class properties
    """
    expense = Expense(1, "school", 200)

    # Checks if properties exist
    assert type(expense.__class__.ID) == property
    assert type(expense.__class__.Category) == property
    assert type(expense.__class__.Amount) == property
    assert type(expense.__class__.Date) == property

    # Tests if properties return correct values
    expense._ID = 20
    assert expense.ID == 20

    expense._Category = "health"
    assert expense.Category == "health"

    expense._Amount = 500
    assert expense.Amount == 500   

    expense._Date = date.today()
    assert expense.Date == date.today()


def test_create_from_dict():
    """
    Tests for the create_from_dict method
    """
    expense = Expense(1, "school", 200)

    # Checks if method exists
    assert hasattr(expense, "create_from_dict")

    # Checks if method returns correct value type (object)
    test_dictionary = {
        'ID': 1,
        'Category': "school",
        'Amount': 200.00,
        'Date': "2021-05-05",
    }

    assert type(expense.create_from_dict(test_dictionary) == object)

    # Checks if returned object is instance of Expense class
    expense_object = expense.create_from_dict(test_dictionary)
    assert isinstance(expense_object, Expense)


def test_get_serializable_field_names():
    """
    Tests for the get_serializable_field_names method
    """
    expense = Expense(1, "school", 200)

    # Checks if method exists
    assert hasattr(expense, "get_serializable_field_names")

    # Checks if method returns correct value
    assert expense.get_serializable_field_names() == ['ID', 'Category', 'Amount', 'Date']

    # Checks if return value is of correct type
    assert type(expense.get_serializable_field_names()) == list 


def test_to_dict():
    """
    Tests for the to_dict method
    """
    expense = Expense(1, "school", 200)

    # Checks if method exists
    assert hasattr(expense, "to_dict")

    # Checks if return value is of correct type
    assert type(expense.to_dict()) == dict
