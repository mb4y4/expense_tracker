import json
import csv
from datetime import datetime, timedelta
from tabulate import tabulate

DATA_FILE = "expenses.json"

def load_expenses():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=4)

def add_expense(amount, category, description=""):
    expenses = load_expenses()
    expense = {
        "amount": amount,
        "category": category,
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"✅ Added: {amount} - {category} ({description})")

def view_expenses(period="all"):
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return

    now = datetime.now()
    if period == "daily":
        expenses = [e for e in expenses if datetime.strptime(e["date"], "%Y-%m-%d %H:%M:%S").date() == now.date()]
    elif period == "weekly":
        week_ago = now - timedelta(days=7)
        expenses = [e for e in expenses if datetime.strptime(e["date"], "%Y-%m-%d %H:%M:%S") >= week_ago]
    elif period == "monthly":
        month_ago = now - timedelta(days=30)
        expenses = [e for e in expenses if datetime.strptime(e["date"], "%Y-%m-%d %H:%M:%S") >= month_ago]

    if not expenses:
        print(f"No {period} expenses found.")
        return

    table = [[e["date"], e["amount"], e["category"], e["description"]] for e in expenses]
    print(tabulate(table, headers=["Date", "Amount", "Category", "Description"], tablefmt="grid"))

def export_csv(filename="expenses.csv"):
    expenses = load_expenses()
    if not expenses:
        print("No expenses to export.")
        return
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "amount", "category", "description"])
        writer.writeheader()
        writer.writerows(expenses)
    print(f"📁 Exported to {filename}")

def menu():
    while True:
        print("\n--- Personal Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Daily Expenses")
        print("3. View Weekly Expenses")
        print("4. View Monthly Expenses")
        print("5. View All Expenses")
        print("6. Export to CSV")
        print("0. Exit")

        choice = input("Enter choice: ")
        if choice == "1":
            amount = float(input("Amount: "))
            category = input("Category: ")
            description = input("Description (optional): ")
            add_expense(amount, category, description)
        elif choice == "2":
            view_expenses("daily")
        elif choice == "3":
            view_expenses("weekly")
        elif choice == "4":
            view_expenses("monthly")
        elif choice == "5":
            view_expenses("all")
        elif choice == "6":
            export_csv()
        elif choice == "0":
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    menu()
