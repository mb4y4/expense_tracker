# db_handler.py
import sqlite3

DB_NAME = "expenses.db"

def add_expense(date, category, amount, currency="KES", description=""):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO expenses (date, category, amount, currency, description) VALUES (?, ?, ?, ?, ?)",
        (date, category, amount, currency, description)
    )

    conn.commit()
    conn.close()

def get_expenses():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_expense(expense_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()
