from db_handler import (
    add_expense, get_expenses, delete_expense,
    search_by_category, search_by_date, search_by_amount
)

def display_expenses(expenses):
    if not expenses:
        print("⚠️ No matching expenses found.")
    else:
        print("\n--- Expenses ---")
        print("{:<5} {:<12} {:<12} {:<10} {:<6} {}".format("ID", "Date", "Category", "Amount", "Curr", "Description"))
        print("-"*60)
        for row in expenses:
            print("{:<5} {:<12} {:<12} {:<10.2f} {:<6} {}".format(row[0], row[1], row[2], row[3], row[4], row[5]))

def main():
    while True:
        print("\n=== Expense Tracker (SQLite) ===")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Delete Expense")
        print("4. Search / Filter")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            date = input("Date (YYYY-MM-DD): ")
            category = input("Category: ")
            amount = float(input("Amount: "))
            currency = input("Currency (default KES): ") or "KES"
            desc = input("Description: ")
            add_expense(date, category, amount, currency, desc)
            print("✅ Expense added!")

        elif choice == "2":
            display_expenses(get_expenses())

        elif choice == "3":
            expense_id = int(input("Enter Expense ID to delete: "))
            delete_expense(expense_id)
            print("🗑️ Expense deleted!")

        elif choice == "4":
            print("\n--- Search / Filter ---")
            print("a) By Category")
            print("b) By Date (YYYY-MM-DD)")
            print("c) By Amount Range")
            sub = input("Choose option: ").lower()

            if sub == "a":
                cat = input("Enter category: ")
                display_expenses(search_by_category(cat))

            elif sub == "b":
                date = input("Enter date (YYYY-MM-DD): ")
                display_expenses(search_by_date(date))

            elif sub == "c":
                min_amt = float(input("Enter minimum amount: "))
                max_amt = float(input("Enter maximum amount: "))
                display_expenses(search_by_amount(min_amt, max_amt))

            else:
                print("⚠️ Invalid choice.")

        elif choice == "5":
            print("👋 Exiting. Goodbye!")
            break

        else:
            print("⚠️ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
