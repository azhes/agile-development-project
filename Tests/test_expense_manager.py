import pytest
from werkzeug.wrappers import ETagResponseMixin
from Models.expense_manager import ExpenseManager
from Models.expense import Expense
from unittest.mock import patch, mock_open


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
    expense1 = Expense(1, "Health", 300, "2020-05-12")
    expense2 = Expense(2, "School", 1000, "2021-04-20")
    expense3 = Expense(3, "Food", 25.6, "2021-4-30")


    # Checks if method exists
    assert hasattr(manager, "add_expense")

    # Tests that method correctly adds expenses to dictionary
    manager.add_expense(expense1)
    manager.add_expense(expense2)
    manager.add_expense(expense3)

    assert manager._expenses[1] == expense1
    assert manager._expenses[2] == expense2
    assert manager._expenses[3] == expense3
    

def test_del_expense():
    """
    Tests for the del_expense method
    """
    manager = ExpenseManager()
    expense1 = Expense(1, "Health", 300, "2020-05-12")
    expense2 = Expense(2, "School", 100.1, "2020-05-11")

    # Checks if method exists
    assert hasattr(manager, "del_expense")

    # Adds expenses 
    manager.add_expense(expense1)
    manager.add_expense(expense2)
    assert manager._expenses[1] == expense1
    assert manager._expenses[2] == expense2

    # Checks that added expenses are deleted correctly
    manager.del_expense(1) 
    manager.del_expense(2) 
    with pytest.raises(KeyError):
        assert manager._expenses[1]
        assert manager._expenses[2]


def test_upd_expense():
    """
    Tests for the upd_expense method
    """
    manager = ExpenseManager()
    expense = Expense(1, "Health", 300, "2020-05-12")
    updated_expense = Expense(1, "School", 100.1, "2020-05-11")

    # Checks if method exists
    assert hasattr(manager, "upd_expense")

    # Adds expense
    manager.add_expense(expense)
    assert manager._expenses[1] == expense

    # Checks that update expense works correctly
    manager.upd_expense(1, updated_expense)
    assert manager._expenses[1] == updated_expense


def test_get_details():
    """
    Tests for the get_details method
    """
    manager = ExpenseManager()
    expense = Expense(1, "School", 200, "2020-02-13")

    # Checks if method exists
    assert hasattr(manager, "get_details")

    # Adds expense
    manager.add_expense(expense)

    # Checks if correct values are returned
    expense_object = manager.get_details(1)
     
    assert getattr(expense_object, "_Category") == "School"
    assert getattr(expense_object, "_Amount") == "200.00"


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

    # Patch to read from a csv add expenses to EM
    with patch('builtins.open', mock_open(read_data="ID,Category,Amount,Date\n1,Health,100.00,2021-05-15\n2,Food,20.00,2021-05-15")) as mock_file:        
        manager.from_csv("test.csv")
        assert manager._expenses[1].ID == 1
        assert manager._expenses[2].Category == "Food"


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

    # Patch to open a csv to read largest id
    with patch('builtins.open', mock_open(read_data="ID,Category,Amount,Date\n1,Health,100.00,2021-05-15\n2,Food,20.00,2021-05-15")) as mock_file:        
        assert manager.read_largest_id("test.csv") == 2


def test_by_month_expense():
    manager = ExpenseManager()
    Expense1 = Expense(1, "Food", 50, "2020-04-29")
    Expense2 = Expense(2, "School", 20, "2021-04-30")
    Expense3 = Expense(3, "Food", 36.6, "2021-05-01")
    Expense4 = Expense(4, "Family", 100, "2021-05-02")
    Expense5 = Expense(5, "Family", 88.8, "2021-01-02")
    Expense6 = Expense(6, "Health", 62, "2021-01-31")

    # Add to the manager
    manager.add_expense(Expense1)
    manager.add_expense(Expense2)
    manager.add_expense(Expense3)
    manager.add_expense(Expense4)
    manager.add_expense(Expense5)
    manager.add_expense(Expense6)

    assert manager.by_month_expense()["Apr"] == 20
    assert manager.by_month_expense()["May"] == 136.6
    assert manager.by_month_expense()["Jan"] == 150.8

def test_by_category():
    manager = ExpenseManager()
    Expense1 = Expense(1, "Food", 50, "2020-04-29")
    Expense2 = Expense(2, "School", 20, "2021-04-30")
    Expense3 = Expense(3, "Food", 36.6, "2021-05-01")
    Expense4 = Expense(4, "Family", 100, "2021-05-02")
    Expense5 = Expense(5, "Family", 88.8, "2021-01-02")
    

    # Add to the manager
    manager.add_expense(Expense1)
    manager.add_expense(Expense2)
    manager.add_expense(Expense3)
    manager.add_expense(Expense4)
    manager.add_expense(Expense5)
    

    assert manager.by_category()["Food"][0] == 36.6
    assert manager.by_category()["Family"][0] == 188.8
    assert manager.by_category()["Health"][0] == 0
    
import pytest
from werkzeug.wrappers import ETagResponseMixin
from Models.expense_manager import ExpenseManager
from Models.expense import Expense


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
    expense1 = Expense(1, "Health", 300, "2020-05-12")
    expense2 = Expense(2, "School", 1000, "2021-04-20")
    expense3 = Expense(3, "Food", 25.6, "2021-4-30")


    # Checks if method exists
    assert hasattr(manager, "add_expense")

    # Tests that method correctly adds expenses to dictionary
    manager.add_expense(expense1)
    manager.add_expense(expense2)
    manager.add_expense(expense3)

    assert manager._expenses[1] == expense1
    assert manager._expenses[2] == expense2
    assert manager._expenses[3] == expense3
    

def test_del_expense():
    """
    Tests for the del_expense method
    """
    manager = ExpenseManager()
    expense1 = Expense(1, "Health", 300, "2020-05-12")
    expense2 = Expense(2, "School", 100.1, "2020-05-11")

    # Checks if method exists
    assert hasattr(manager, "del_expense")

    # Adds expenses 
    manager.add_expense(expense1)
    manager.add_expense(expense2)
    assert manager._expenses[1] == expense1
    assert manager._expenses[2] == expense2

    # Checks that added expenses are deleted correctly
    manager.del_expense(1) 
    manager.del_expense(2) 
    with pytest.raises(KeyError):
        assert manager._expenses[1]
        assert manager._expenses[2]



def test_upd_expense():
    """
    Tests for the upd_expense method
    """
    manager = ExpenseManager()
    expense = Expense(1, "Health", 300, "2020-05-12")
    updated_expense = Expense(1, "School", 100.1, "2020-05-11")

    # Checks if method exists
    assert hasattr(manager, "upd_expense")

    # Adds expense
    manager.add_expense(expense)
    assert manager._expenses[1] == expense

    # Checks that update expense works correctly
    manager.upd_expense(1, updated_expense)
    assert manager._expenses[1] == updated_expense


def test_get_details():
    """
    Tests for the get_details method
    """
    manager = ExpenseManager()
    expense = Expense(1, "School", 200, "2020-02-13")

    # Checks if method exists
    assert hasattr(manager, "get_details")

    # Adds expense
    manager.add_expense(expense)

    # Checks if correct values are returned
    expense_object = manager.get_details(1)
     
    assert getattr(expense_object, "_Category") == "School"
    assert getattr(expense_object, "_Amount") == "200.00"


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

def test_override_to_csv():
    """
    Tests for the override_to_csv method
    """
    manager = ExpenseManager()

    # Checks if method exists
    assert hasattr(manager, "override_to_csv")


def test_read_largest_id():
    """
    Tests for the read_largest_id method
    """
    manager = ExpenseManager()

    # Checks if method exists
    assert hasattr(manager, "read_largest_id")
    

def test_by_month_expense():
    """
    Tests for the by_month_expense method
    """
    manager = ExpenseManager()
    Expense1 = Expense(1, "Food", 50, "2020-04-29")
    Expense2 = Expense(2, "School", 20, "2021-04-30")
    Expense3 = Expense(3, "Food", 36.6, "2021-05-01")
    Expense4 = Expense(4, "Family", 100, "2021-05-02")
    Expense5 = Expense(5, "Family", 88.8, "2021-01-02")
    Expense6 = Expense(6, "Health", 62, "2021-01-31")

    # Add to the manager
    manager.add_expense(Expense1)
    manager.add_expense(Expense2)
    manager.add_expense(Expense3)
    manager.add_expense(Expense4)
    manager.add_expense(Expense5)
    manager.add_expense(Expense6)

    assert manager.by_month_expense()["Apr"] == 20
    assert manager.by_month_expense()["May"] == 136.6
    assert manager.by_month_expense()["Jan"] == 150.8

def test_by_category():
    """
    Tests for the by_category method
    """
    manager = ExpenseManager()
    Expense1 = Expense(1, "Food", 50, "2020-04-29")
    Expense2 = Expense(2, "School", 20, "2021-04-30")
    Expense3 = Expense(3, "Food", 36.6, "2021-05-01")
    Expense4 = Expense(4, "Family", 100, "2021-05-02")
    Expense5 = Expense(5, "Family", 88.8, "2021-01-02")
    

    # Add to the manager
    manager.add_expense(Expense1)
    manager.add_expense(Expense2)
    manager.add_expense(Expense3)
    manager.add_expense(Expense4)
    manager.add_expense(Expense5)
    

    assert manager.by_category()["Food"][0] == 36.6
    assert manager.by_category()["Family"][0] == 188.8
    assert manager.by_category()["Health"][0] == 0
    
