from flask import Flask, render_template, request, redirect, url_for
from db_handler import init_db, add_expense, get_all_expenses, delete_expense

app = Flask(__name__)

# Define budgets for categories
budgets = {
    "Food": 500,
    "Transport": 300,
    "Entertainment": 200,
    "Utilities": 400,
    "Other": 150
}

@app.route("/")
def index():
    expenses = get_all_expenses()
    
    # Calculate totals per category
    category_totals = {cat: 0 for cat in budgets}
    for exp in expenses:
        amount = exp[1]  # correct, amount
        category = exp[2]  # correct, category string
        if category in category_totals:
            category_totals[category] += amount

    
    return render_template("index.html", expenses=expenses, budgets=budgets, category_totals=category_totals)

@app.route("/add", methods=["POST"])
def add():
    amount = float(request.form["amount"])
    category = request.form["category"]
    description = request.form["description"]  # <-- correct field
    add_expense(amount, category, description)
    return redirect(url_for("index"))


@app.route("/delete/<int:expense_id>")
def delete(expense_id):
    delete_expense(expense_id)
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
