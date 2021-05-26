from Models.expense import Expense
import csv
from datetime import datetime, timedelta


class ExpenseManager:

    def __init__(self):
        self._expenses = {}

    
    def add_expense(self, expense):
        """ Add a new expense to the Expense Manager

        :param expense: A new expense from user
        :type expense: Expense
        :raises TypeError: Valid for class Expense only
        """
        if not isinstance(expense, Expense):
            raise TypeError("Invalid expense type!")
        self._expenses[expense.ID] = expense


    def del_expense(self, expenseID):
        """ Delete the expense from Expense Manager based on the expense ID"""
        self._expenses.pop(expenseID)
    

    def upd_expense(self, expenseID, expense):
        """ Update the expense from Expense Manager based on the expense ID"""
        self._expenses[expenseID] = expense


    def get_expenses(self):
        """Return a list of expenses (in dict) that stored inside the Expense Maanger """

        expenses_list = []
        for (key, value) in self._expenses.items():
            expenses_list.append(value)
        return [ expense.to_dict() for expense in expenses_list]


    def get_details(self, ID):
        """
        Returns attribute values of expense using its ID

        :param budget
        :type budget: int
        """
        return self._expenses.get(ID)
        

    def from_csv(self, csv_file):
        """Get data from a csv file

        :param csv_file: csv file to get from
        :type csv_file, i.e. the filepath
        """
        with open(csv_file, "r") as f:
            reader = csv.DictReader(f)
            for item in reader:
                expense = Expense.create_from_dict(item)
                self.add_expense(expense)


    def to_csv(self, csv_file):
        """Append to a csv file"""
        fields = Expense.get_serializable_field_names()
        with open(csv_file, "a", newline="") as f:
            writer = csv.DictWriter(f, fields)
            for expense in self._expenses.values():
                writer.writerow(expense.to_dict())


    def override_to_csv(self, csv_file):
        """Write to a csv file"""
        fields = Expense.get_serializable_field_names()
        with open(csv_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fields)
            writer.writeheader()
            for expense in self._expenses.values():
                writer.writerow(expense.to_dict())


    def read_largest_id(self, csv_file):
        """Get largest id from csv_file

        :param csv_file: csv file to get from
        :type csv_file, i.e. the filepath
        """
        id = []
        with open(csv_file, "r") as f:
            reader = csv.DictReader(f)
            for item in reader:
                expense = Expense.create_from_dict(item)
                id.append(expense.ID)
            id.sort(reverse=True)
        # Check if the csv have no record at all
        if len(id) == 0:
            largest_ID = 0
        else:
            largest_ID = id[0]
        return largest_ID
            

    def by_month_expense(self):
        """ Calculate the expenses by month (last 1 year)"""
        
        dict_month = {
            "Jan": 0.0,
            "Feb": 0.0,
            "Mar": 0.0,
            "Apr": 0.0,
            "May": 0.0,
            "Jun": 0.0,
            "Jul": 0.0,
            "Aug": 0.0,
            "Sep": 0.0,
            "Oct": 0.0,
            "Nov": 0.0,
            "Dec": 0.0
            }
        TODAY = datetime.today()

        for (key, value) in self._expenses.items():
            if TODAY - value.Date <= timedelta(365):
                if value.Date.month == 1:
                    dict_month["Jan"] = dict_month["Jan"] + float(value.Amount)
                if value.Date.month == 2:
                    dict_month["Feb"] = dict_month["Feb"] + float(value.Amount)
                if value.Date.month == 3:
                    dict_month["Mar"] = dict_month["Mar"] + float(value.Amount)
                if value.Date.month == 4:
                    dict_month["Apr"] = dict_month["Apr"] + float(value.Amount)    
                if value.Date.month == 5:
                    dict_month["May"] = dict_month["May"] + float(value.Amount)
                if value.Date.month == 6:
                    dict_month["Jun"] = dict_month["Jun"] + float(value.Amount)
                if value.Date.month == 7:
                    dict_month["Jul"] = dict_month["Jul"] + float(value.Amount)
                if value.Date.month == 8:
                    dict_month["Aug"] = dict_month["Aug"] + float(value.Amount)
                if value.Date.month == 9:
                    dict_month["Sep"] = dict_month["Sep"] + float(value.Amount)
                if value.Date.month == 10:
                    dict_month["Oct"] = dict_month["Oct"] + float(value.Amount)
                if value.Date.month == 11:
                    dict_month["Nov"] = dict_month["Nov"] + float(value.Amount)
                if value.Date.month == 12:
                    dict_month["Dec"] = dict_month["Dec"] + float(value.Amount)

        return dict_month


    def by_category(self):
        """ Calculate the expenses by caetgory """

        # 1st element is subtotal; 2nd element is percentage
        dict_category = {
            "School": [0.0, 0.0],
            "Food": [0.0, 0.0],
            "Health": [0.0, 0.0],
            "Family": [0.0, 0.0]}
        TODAY = datetime.today()
        Total = 0

        # Calculate the total amouunt
        for (key, value) in self._expenses.items():
            if TODAY - value.Date <= timedelta(365):
                Total = Total + float(value.Amount)

        for (key, value) in self._expenses.items():
            if TODAY - value.Date <= timedelta(365):
                if value.Category == "School":
                    dict_category["School"][0] = dict_category["School"][0] + float(value.Amount)
                    dict_category["School"][1] = format(dict_category["School"][0] / Total * 100, ".2f")
                if value.Category == "Food":
                    dict_category["Food"][0] = dict_category["Food"][0] + float(value.Amount)
                    dict_category["Food"][1] = format(dict_category["Food"][0] / Total * 100, ".2f")
                if value.Category == "Health":
                    dict_category["Health"][0] = dict_category["Health"][0] + float(value.Amount)
                    dict_category["Health"][1] = format(dict_category["Health"][0] / Total * 100, ".2f")
                if value.Category == "Family":
                    dict_category["Family"][0] = dict_category["Family"][0] + float(value.Amount)
                    dict_category["Family"][1] = format(dict_category["Family"][0] / Total * 100, ".2f")
            
        return dict_category


############################################
if __name__ == "__main__":
    EM = ExpenseManager()
    EM.from_csv("expense.csv")

    print(EM.get_expenses())    
    print(EM.read_largest_id("expense.csv"))
