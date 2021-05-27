from flask import Flask, request, render_template, url_for, redirect, flash
import csv
from Models.expense import Expense
from Models.expense_manager import ExpenseManager
from time import strftime


app = Flask(__name__)
app.secret_key = b'ooo_5#y2L"F4Q9858z\n\xec]/'

# Database filename: csv file for expense and balance/budget
expense_csv = "Models/expense.csv"
balance_csv = "data.csv"


def create_csv(balance, budget):
    """
    Creates data.csv for storing balance and budget
    :param balance: balance to be updated
    :type balance: float

    :param budget: budget to be updated
    :type budget: float
    """
    with open(balance_csv, 'w', newline = '') as f:
        writer = csv.writer(f)
        rows = [balance, budget]

        fields = ["Balance", "Budget"]
            
        # Writes fields and rows to csv
        writer.writerow(fields)
        writer.writerow(rows)


def add_to_csv(balance, budget):
    """ 
    Adds balance and budget to the csv file
    :param balance: balance to be updated
    :type balance: float

    :param budget: budget to be updated
    :type budget: float
    """
    # Appends to data.csv instead of writing, which would replace existing entries
    with open(balance_csv, 'a', newline = '') as f:
        writer = csv.writer(f)
        rows = [balance, budget]
        writer.writerow(rows)


def from_csv(csv_file):
    """
    Loads balance and budget from the csv file 
    :param csv_file: csv file with balance/budget
    :type csv_file: str

    :return: Latest balance and budget from the csv file
    :rtype: dict
    """
    balanceBudget = {}
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        for item in reader:
            balanceBudget["balance"] = format(float(item["balance"]), ".2f")
            balanceBudget["budget"] = format(float(item["budget"]), ".2f")
    
    return balanceBudget
                

def list_all_expenses():
    """ 
    Lists all expenses in the expenses csv file
    :return: All expenses records
    :rtype: dict
    """
    EM = ExpenseManager()
    EM.from_csv(expense_csv)
    return {"expenses": EM.get_expenses()}
    

def display_expense_by_month():
    """ 
    Summarize all expesnses by month 
    :return: All expenses subtotal in last 12 months
    :rtype: dict
    """
    EM = ExpenseManager()
    EM.from_csv(expense_csv)
    return EM.by_month_expense()


def display_expense_by_category():
    """ 
    Summarize all expenses by category
    :return: All expenses subtotal by category in last 12 months, with percentage
    :rtype: dict
    """
    
    EM = ExpenseManager()
    EM.from_csv(expense_csv)
    return EM.by_category()


def delete_expense(ID):
    """ 
    Delete the expense record from the list
    :param ID: ID of expense to be deleted
    :type ID: int

    :return: None
    :rtype: None
    """
    # Load the list of expenses from csv, then put it into EM to manipulate
    # Finally put it back to the csv
    EM = ExpenseManager()
    EM.from_csv(expense_csv)
    EM.del_expense(ID)
    EM.override_to_csv(expense_csv)


def update_expense(ID, category, amount, date):
    """ 
    Updates the specified expense
    :param ID: ID of expense to be updated
    :type ID: int
    
    :return: None
    :rtype: None
    """
    EM = ExpenseManager()
    EM.from_csv(expense_csv)

    expense = Expense(ID, category, amount, date)
    EM.upd_expense(ID, expense)
    EM.override_to_csv(expense_csv)


##################################################################
### Routes from here ###

@app.route('/')
def index():  
    return render_template(
        "main.html", 
        expenses=list_all_expenses(), 
        balanceBudget=from_csv(balance_csv), 
        byMonth=display_expense_by_month(),
        byCategory=display_expense_by_category(),
        )


@app.route("/delete/<int:ID>")
def delete(ID):
    EM = ExpenseManager()
    EM.from_csv(expense_csv)
    expense = EM.get_details(ID)
    
    category = getattr(expense, "_Category")
    amount = getattr(expense, "_Amount")
    date = getattr(expense, "_Date")

    # Adds expense amount back to balance
    bal_dict=from_csv(balance_csv)
    bal_dict["balance"] = float(bal_dict["balance"]) + float(amount)

    # Save expense
    EM.to_csv(expense_csv)

    # Save balance, budget
    add_to_csv(bal_dict["balance"], bal_dict["budget"])

    delete_expense(ID)
    flash(f'Expense #{ID} has been deleted!')
    flash(f'${amount} added to balance')
    return redirect(url_for("index"))


@app.route("/update/<int:ID>")
def edit(ID):
    EM = ExpenseManager()
    EM.from_csv(expense_csv)
    expense = EM.get_details(ID)
    
    category = getattr(expense, "_Category")
    amount = getattr(expense, "_Amount")
    date = getattr(expense, "_Date")
    category=category.lower()
    
    return render_template("update.html", ID=ID,category=category, amount=amount, date=date)


@app.route("/update/<int:ID>", methods=['POST'])
def update(ID):
    try:
        category = request.form['category']
        amount = float(request.form['amount'])
        date = request.form['date']
    except ValueError:
        flash("Please enter a valid number for expense amount")
        return redirect(url_for("edit", ID=ID))
    except KeyError:
        return redirect(url_for("index"))

    flash(f'Expense #{ID} has been updated!')
    
    EM = ExpenseManager()
    EM.from_csv(expense_csv)
    expense = EM.get_details(ID)
    original_expense = float(getattr(expense, "_Amount"))

    # Updates balance amount
    bal_dict=from_csv(balance_csv)
    original_balance = float(bal_dict["balance"])
    updated_expense = amount

    # Deducts from balance (expense amount increased)
    if updated_expense > original_expense:  
        amount_to_change = updated_expense - original_expense      
        updated_balance = original_balance - amount_to_change
        flash(f'${float(amount_to_change)} deducted from balance')

    # Adds to balance (expense amount decreased)
    elif updated_expense < original_expense:
        amount_to_change = original_expense - updated_expense
        updated_balance = original_balance + amount_to_change
        flash(f'${float(amount_to_change)} added to balance')
    else:
        updated_balance = original_balance

    # Save expense
    EM.to_csv(expense_csv)

    # Save balance, budget
    add_to_csv(updated_balance, bal_dict["budget"])

    update_expense(ID, category, amount, date)
    
    monthly_expenses = display_expense_by_month()
    current_month = strftime('%b')
    
    if float(bal_dict["budget"]) < float(monthly_expenses[current_month]):
            flash("Your current month expenses have exceeded your budget!")

    return redirect(url_for("index"))


@app.route("/add",  methods=['POST'])
def expense():
    ## Expense ##

    # Get input from html
    try:
        category = request.form['category']
    except KeyError:
        flash("Please select a category")
        return redirect(url_for("index"))

    try:
        amount = float(request.form['amount'])
    except ValueError:
        flash("Please enter a valid number for expense amount")
        return redirect(url_for("index"))

    

    if category != "":
        # Store as a class Expense object
        EM = ExpenseManager()
        Next_ID = EM.read_largest_id(expense_csv) + 1 # Assign the next ID#
        expense = Expense(Next_ID, category, amount)
        
        # Add the expense into the Expense Manager
        EM.add_expense(expense)
        
        # Save expense
        EM.to_csv(expense_csv)

        # Deduct expense amount from balance
        monthly_expenses = display_expense_by_month()
        current_month = strftime('%b')
        bal_dict=from_csv(balance_csv)
        bal_dict["balance"] = float(bal_dict["balance"]) - float(expense.Amount)
        if float(bal_dict["budget"]) < float(monthly_expenses[current_month]):
            flash("Your current month expenses have exceeded your budget!")
                

        # Save balance, budget
        add_to_csv(bal_dict["balance"], bal_dict["budget"])
    elif len(category) == 0:
        flash("Category can't be left empty")
        return redirect(url_for("index"))

    flash(f'Expense #{Next_ID} has been added!')
    flash(f'${expense.Amount} deducted from balance')
    return redirect(url_for("index"))


@app.route('/', methods=['POST'])
def balanceBudget():
    ## Balance ##
    try:
        balance = float(request.form['balance'])
    except ValueError:
        balance = request.form['balance']
        if balance == "":
            balance = from_csv(balance_csv)["balance"]
        else:
            flash("Please enter a valid number for balance amount")
        balance = from_csv(balance_csv)["balance"]

    
    try:
        budget = float(request.form['budget'])
    except ValueError:
        budget = request.form['budget']
        if budget == "":
            budget = from_csv(balance_csv)["budget"]
        else:
            flash("Please enter a valid number for budget amount")
        budget = from_csv(balance_csv)["budget"]
        

    # Check if the input box is empty or non-integer value entered
    try: 
        with open(balance_csv, 'a') as f:
            add_to_csv(balance, budget)
    except FileNotFoundError:
        create_csv(balance, budget)
    
    return redirect(url_for("index"))
    


if __name__ == "__main__":
    app.run(debug=True)

