from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DB_NAME = "expenses.db"

# Home route (list expenses)
@app.route("/")
def index():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, amount, currency, description, date FROM expenses")
    expenses = cursor.fetchall()
    conn.close()
    return render_template("index.html", expenses=expenses)

# Add expense
@app.route("/add", methods=["POST"])
def add():
    category = request.form["category"]
    amount = float(request.form["amount"])
    currency = request.form["currency"]
    description = request.form["description"]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (category, amount, currency, description, date) VALUES (?, ?, ?, ?, DATE('now'))",
        (category, amount, currency, description)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
