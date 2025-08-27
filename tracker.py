import json
import os
from datetime import datetime

EXPENSES_FILE = "expenses.json"
SETTINGS_FILE = "settings.json"


def load_data():
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, "r") as f:
            return json.load(f)
    return []


def save_data(data):
    with open(EXPENSES_FILE, "w") as f:
        json.dump(data, f, indent=4)


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {"currency": "KES", "budgets": {}}  # defaults


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)


def add_expense():
    data = load_data()
    settings = load_settings()

    category = input("Enter category (e.g., Food, Transport): ").title()
    amount = float(input("Enter amount: "))
    description = input("Enter description: ")
    currency = settings.get("currency", "KES")

    expense = {
        "id": len(data) + 1,
        "category": category,
        "amount": amount,
        "currency": currency,
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    data.append(expense)
    save_data(data)

    # Budget check
    budget = settings["budgets"].get(category)
    if budget:
        total = sum(e["amount"] for e in data if e["category"] == category)
        if total > budget:
            print(f"⚠️ Warning: You have exceeded your budget for {category} ({total}/{budget} {currency})")

    print("✅ Expense added successfully!")


def view_expenses():
    data = load_data()
    if not data:
        print("No expenses found.")
        return
    for e in data:
        print(f"[{e['id']}] {e['date']} | {e['category']}: {e['amount']} {e['currency']} - {e['description']}")


def summary_by_category():
    data = load_data()
    if not data:
        print("No expenses found.")
        return
    summary = {}
    for e in data:
        summary[e["category"]] = summary.get(e["category"], 0) + e["amount"]

    settings = load_settings()
    currency = settings.get("currency", "KES")

    print("\n--- Category Summary ---")
    for cat, total in summary.items():
        print(f"{cat}: {total} {currency}")


def search_expenses():
    data = load_data()
    if not data:
        print("No expenses found.")
        return

    choice = input("Search by (1) Category or (2) Amount greater than: ")
    if choice == "1":
        category = input("Enter category: ").title()
        results = [e for e in data if e["category"] == category]
    elif choice == "2":
        amount = float(input("Enter minimum amount: "))
        results = [e for e in data if e["amount"] >= amount]
    else:
        print("Invalid choice.")
        return

    if results:
        for e in results:
            print(f"[{e['id']}] {e['date']} | {e['category']}: {e['amount']} {e['currency']} - {e['description']}")
    else:
        print("No matching expenses found.")


def delete_expense():
    data = load_data()
    view_expenses()
    exp_id = int(input("Enter the ID of the expense to delete: "))
    data = [e for e in data if e["id"] != exp_id]
    # reassign IDs
    for i, e in enumerate(data, start=1):
        e["id"] = i
    save_data(data)
    print("✅ Expense deleted successfully!")


def update_expense():
    data = load_data()
    view_expenses()
    exp_id = int(input("Enter the ID of the expense to update: "))
    for e in data:
        if e["id"] == exp_id:
            print("Leave blank to keep current value.")
            category = input(f"New category ({e['category']}): ") or e["category"]
            amount = input(f"New amount ({e['amount']}): ")
            description = input(f"New description ({e['description']}): ")

            if amount:
                e["amount"] = float(amount)
            e["category"] = category
            e["description"] = description

            save_data(data)
            print("✅ Expense updated successfully!")
            return
    print("Expense not found.")


def set_currency():
    settings = load_settings()
    currency = input("Enter default currency (e.g., KES, USD, EUR): ").upper()
    settings["currency"] = currency
    save_settings(settings)
    print(f"✅ Default currency set to {currency}")


def set_budget():
    settings = load_settings()
    category = input("Enter category to set budget for: ").title()
    amount = float(input("Enter budget amount: "))
    settings["budgets"][category] = amount
    save_settings(settings)
    print(f"✅ Budget set for {category}: {amount} {settings['currency']}")


def main():
    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Summary by Category")
        print("4. Search Expenses")
        print("5. Delete Expense")
        print("6. Update Expense")
        print("7. Set Currency")
        print("8. Set Budget")
        print("9. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            summary_by_category()
        elif choice == "4":
            search_expenses()
        elif choice == "5":
            delete_expense()
        elif choice == "6":
            update_expense()
        elif choice == "7":
            set_currency()
        elif choice == "8":
            set_budget()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
