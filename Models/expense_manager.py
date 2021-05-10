from Models.expense import Expense
# from expense import Expense
import csv


class ExpenseManager:

    def __init__(self):
        self._expenses = {}

    
    def add_expense(self, expense):
        if not isinstance(expense, Expense):
            raise TypeError("Invalid expense type!")
        self._expenses[expense.ID] = expense


    def del_expense(self, expenseID):
        """ Delete the expense from Expense Manager based on the expense ID"""
        self._expenses.pop(expenseID)


    def get_expenses(self):
        """Return a list of expenses (in dict) that stored inside the Expense Maanger """

        expenses_list = []
        for (key, value) in self._expenses.items():
            expenses_list.append(value)
        return [ expense.to_dict() for expense in expenses_list]


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
            # writer.writeheader()
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
            


############################################
if __name__ == "__main__":
    EM = ExpenseManager()
    EM.from_csv("expense.csv")

    print(EM.get_expenses())    
    print(EM.read_largest_id("expense.csv"))

    # EM.del_expense(2)
    # print(EM.get_expenses())    