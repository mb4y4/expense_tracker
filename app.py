from flask import Flask, render_template, request, redirect, url_for
from db_handler import init_db, add_expense, get_all_expenses, delete_expense

app = Flask(__name__)
init_db()

# Predefined categories
categories = [
    "Food",
    "Transport",
    "Entertainment",
    "Bills",
    "Shopping",
    "Miscellaneous"
]

# Example budgets
budgets = {
    "Food": 2000,
    "Transport": 1500,
    "Entertainment": 1000,
    "Bills": 3000,
    "Shopping": 2500,
    "Miscellaneous": 1000
}

@app.route("/", methods=["GET"])
def index():
    expenses = get_all_expenses()

    # Initialize category totals
    category_totals = {category: 0 for category in categories}

    # Sum up expenses by category
    for exp in expenses:
        category_totals[exp["category"]] += float(exp["amount"])

    return render_template(
        "index.html",
        expenses=expenses,
        categories=categories,
        budgets=budgets,
        category_totals=category_totals
    )

@app.route("/add", methods=["POST"])
def add():
    description = request.form["description"]
    amount = float(request.form["amount"])
    category = request.form["category"]
    add_expense(description, amount, category)
    return redirect(url_for("index"))

@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete(expense_id):
    delete_expense(expense_id)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
