from db_handler import add_expense, get_expenses, delete_expense

def main():
    while True:
        print("\n=== Expense Tracker (SQLite) ===")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Delete Expense")
        print("4. Exit")

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
            expenses = get_expenses()
            if not expenses:
                print("⚠️ No expenses found.")
            else:
                print("\n--- All Expenses ---")
                print("{:<5} {:<12} {:<12} {:<10} {:<6} {}".format("ID", "Date", "Category", "Amount", "Curr", "Description"))
                print("-"*60)
                for row in expenses:
                    print("{:<5} {:<12} {:<12} {:<10.2f} {:<6} {}".format(row[0], row[1], row[2], row[3], row[4], row[5]))

        elif choice == "3":
            expense_id = int(input("Enter Expense ID to delete: "))
            delete_expense(expense_id)
            print("🗑️ Expense deleted!")

        elif choice == "4":
            print("👋 Exiting. Goodbye!")
            break

        else:
            print("⚠️ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
