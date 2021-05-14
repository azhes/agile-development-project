from flask import Flask, request, render_template, url_for, redirect, flash
import csv
from Models.expense import Expense
from Models.expense_manager import ExpenseManager


app = Flask(__name__)
app.secret_key = b'ooo_5#y2L"F4Q9858z\n\xec]/'

# Database filename: csv file for expense and balance/budget
expense_csv = "Models\expense.csv"
balance_csv = "data.csv"


def create_csv(balance, budget):
        with open(balance_csv, 'w', newline = '') as f:
            writer = csv.writer(f)
            rows = [balance, budget]

            fields = ["Balance", "Budget"]
            
            # Writes fields and rows to csv
            writer.writerow(fields)
            writer.writerow(rows)


def add_to_csv(balance, budget):
    """ Add balance and budget to the csv file

    :param balance: balance that to be updated
    :type balance: float
    :param budget: budget that to be updated
    :type budget: float
    """
    # Appends to data.csv instead of writing, which would replace existing entries
    with open(balance_csv, 'a', newline = '') as f:
        writer = csv.writer(f)
        rows = [balance, budget]
        writer.writerow(rows)


def from_csv(csv_file):
    """ Load the balance and budget from the csv file 
    
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
    """ List all expenses in the csv file

    :return: All expenses records
    :rtype: dict
    """
    EM = ExpenseManager()
    EM.from_csv(expense_csv)
    return {"expenses": EM.get_expenses()}
    

def display_expense_by_month():
    """ Summarize all expesnses by month 

    :return: All expenses subtotal in last 12 months
    :rtype: dict
    """
    EM = ExpenseManager()
    EM.from_csv(expense_csv)
    return EM.by_month_expense()


def display_expense_by_category():
    """ Summarize all expenses by category

    :return: All expenses subtotal by category in last 12 months, with percentage
    :rtype: dict
    """
    EM = ExpenseManager()
    EM.from_csv(expense_csv)
    return EM.by_category()


def delete_expense(ID):
    """ Delete the expense record from the list

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
    delete_expense(ID)
    flash(f'Expense #{ID} has been deleted!')
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
        return redirect(url_for("index"))
    except KeyError:
        return redirect(url_for("index"))

    update_expense(ID, category, amount, date)
    flash(f'Expense #{ID} has been updated!')
    return redirect(url_for("index"))


@app.route("/add",  methods=['POST'])
def expense():
    ## Expense ##

    # Get input from html
    try:
        category = request.form['category']
        amount = float(request.form['amount'])
    except ValueError:
        return redirect(url_for("index"))
    except KeyError:
        return redirect(url_for("index"))
        

    if category != "":
        # Store as a class Expense object
        EM = ExpenseManager()
        Next_ID = EM.read_largest_id(expense_csv) + 1 # Assign the next ID#
        expense = Expense(Next_ID, category, amount)
        
        # Add the expense into the Expense Manager
        EM.add_expense(expense)
        
        # Deduct expense amount from balance
        bal_dict=from_csv(balance_csv)
        bal_dict["balance"] = float(bal_dict["balance"]) - float(expense.Amount)
        
        # Save expense
        EM.to_csv(expense_csv)

        # Save balance, budget
        add_to_csv(bal_dict["balance"], bal_dict["budget"])
    flash(f'Expense #{Next_ID} has been added!')
    return redirect(url_for("index"))


@app.route('/', methods=['POST'])
def balanceBudget():
    ## Balance ##
    balance = request.form['balance']
    budget = request.form['budget']

    # Check if the input box is empty
    if balance == "":
        balance = from_csv(balance_csv)["balance"]
    if budget == "":
        budget = from_csv(balance_csv)["budget"]

    try: 
        with open(balance_csv, 'a') as f:
            add_to_csv(balance, budget)
    except FileNotFoundError:
        create_csv(balance, budget)
    
    return redirect(url_for("index"))
    





if __name__ == "__main__":
    app.run(debug=True)
