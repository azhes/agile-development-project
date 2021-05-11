from flask import Flask, request, render_template, url_for, redirect
import csv
from Models.expense import Expense
from Models.expense_manager import ExpenseManager


app = Flask(__name__)

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
        # Appends to data.csv instead of writing, which would replace existing entries
        with open(balance_csv, 'a', newline = '') as f:
            writer = csv.writer(f)
            rows = [balance, budget]
            writer.writerow(rows)


def from_csv(csv_file):
    """ Load the balance and budget from the csv file """
    balanceBudget = {}
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        for item in reader:
            balanceBudget["balance"] = format(float(item["balance"]), ".2f")
            balanceBudget["budget"] = format(float(item["budget"]), ".2f")
    
    return balanceBudget
                

def list_all_expenses():
    EM = ExpenseManager()
    EM.from_csv(expense_csv)
    return {"expenses": EM.get_expenses()}


def delete_expense(ID):
    """ Delete the expense record from the list"""
    # Load the list of expenses from csv, then put it into EM to manipulate
    # Finally put it back to the csv
    EM = ExpenseManager()
    EM.from_csv(expense_csv)
    EM.del_expense(ID)
    EM.override_to_csv(expense_csv)


@app.route("/delete/<int:ID>")
def delete(ID):
    delete_expense(ID)
    return redirect(url_for("index"))
    # return render_template("main.html", expenses=list_all_expenses(), balanceBudget=from_csv(balance_csv))


@app.route('/')
def index():  
    return render_template("main.html", expenses=list_all_expenses(), balanceBudget=from_csv(balance_csv))


@app.route('/', methods=['POST'])
def expense():
    ## Expense ##

    # Get input from html
    try:
        category = request.form['category']
        amount = float(request.form['amount'])
    except ValueError:
        return render_template("main.html", expenses=list_all_expenses(), balanceBudget=from_csv(balance_csv))
    except KeyError:
        balanceBudget()
        return render_template("main.html", expenses=list_all_expenses(), balanceBudget=from_csv(balance_csv))

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

    balanceBudget()
    return render_template("main.html", expenses=list_all_expenses(), balanceBudget=from_csv(balance_csv))


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
    

    return render_template("main.html", expenses=list_all_expenses(), balanceBudget=from_csv(balance_csv))





if __name__ == "__main__":
    app.run(debug=True)
