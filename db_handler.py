import sqlite3

DB_NAME = "expenses.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  description TEXT,
                  amount REAL,
                  category TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS budgets
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  category TEXT UNIQUE,
                  budget REAL)''')
    conn.commit()
    conn.close()

def add_expense(description, amount, category):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO expenses (description, amount, category) VALUES (?, ?, ?)", 
              (description, float(amount), category))
    conn.commit()
    conn.close()

def get_all_expenses():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, description, amount, category FROM expenses")
    rows = c.fetchall()
    conn.close()
    # Cast amount to float always
    return [(row[0], row[1], float(row[2]), row[3]) for row in rows]

def delete_expense(expense_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

def set_budget(category, budget):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO budgets (category, budget) VALUES (?, ?)", 
              (category, float(budget)))
    conn.commit()
    conn.close()

def get_budgets():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT category, budget FROM budgets")
    rows = c.fetchall()
    conn.close()
    # Cast budget to float always
    return {row[0]: float(row[1]) for row in rows}
