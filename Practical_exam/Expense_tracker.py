import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class ExpenseTracker:
    """Manage expenses, summaries, filters, CSV storage, and charts."""

    COLUMNS = ["Date", "Amount", "Category", "Description"]
    VALID_CATEGORIES = [
        "Food", "Transport", "Utilities", "Entertainment",
        "Shopping", "Education", "Health", "Other"
    ]

    def __init__(self, filename="expenses.csv"):
        self.filename = filename
        self.df = pd.DataFrame(columns=self.COLUMNS)
        self.load_data()

    def load_data(self):
        """Load expense records from CSV and validate their columns."""
        if not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0:
            self.df = pd.DataFrame(columns=self.COLUMNS)
            return

        try:
            data = pd.read_csv(self.filename)
            for column in self.COLUMNS:
                if column not in data.columns:
                    data[column] = ""

            data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
            data["Amount"] = pd.to_numeric(data["Amount"], errors="coerce")
            data["Category"] = data["Category"].fillna("").astype(str).str.strip().str.title()
            data["Description"] = data["Description"].fillna("").astype(str)

            data = data.dropna(subset=["Date", "Amount"])
            data = data[(data["Amount"] > 0) & (data["Category"] != "")]
            self.df = data[self.COLUMNS].reset_index(drop=True)
        except (pd.errors.ParserError, OSError, UnicodeDecodeError) as error:
            print(f"Error loading CSV file: {error}")
            self.df = pd.DataFrame(columns=self.COLUMNS)

    def save_data(self):
        """Persist records to the configured CSV file."""
        self.df.to_csv(self.filename, index=False, date_format="%Y-%m-%d")

    @classmethod
    def get_valid_categories(cls):
        """Return supported categories."""
        return cls.VALID_CATEGORIES.copy()

    @staticmethod
    def _parse_date(value):
        """Convert a date string into a pandas Timestamp."""
        return pd.to_datetime(value, errors="raise")

    def add_expense(self, date, amount, category, description):
        """Validate and add an expense."""
        try:
            amount = float(amount)
            if not np.isfinite(amount) or amount <= 0:
                print("Error: Amount must be a positive number.")
                return False

            category = str(category).strip().title()
            if category not in self.VALID_CATEGORIES:
                print("Error: Invalid category.")
                print("Valid categories:", ", ".join(self.get_valid_categories()))
                return False

            date_value = self._parse_date(date)
            new_row = pd.DataFrame([{
                "Date": date_value,
                "Amount": amount,
                "Category": category,
                "Description": str(description).strip()
            }])

            self.df = pd.concat([self.df, new_row], ignore_index=True)
            self.save_data()
            print("Expense successfully added!")
            return True
        except (ValueError, TypeError, OverflowError):
            print("Error: Enter a valid date (YYYY-MM-DD) and numeric amount.")
            return False
        except OSError as error:
            print(f"Error saving expense: {error}")
            return False

    def get_summary(self):
        """Show totals, averages, category totals, percentages, and monthly averages."""
        if self.df.empty:
            print("No expense data available.")
            return

        total = float(self.df["Amount"].sum())
        average = float(self.df["Amount"].mean())
        print("\n--- EXPENSE SUMMARY ---")
        print(f"Total Expenses: {total:.2f}")
        print(f"Average Expense: {average:.2f}")

        print("\nCategory-wise Spending:")
        category_totals = self.df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
        for category, amount in category_totals.items():
            percentage = (amount / total * 100) if total else 0
            print(f"{category}: {amount:.2f} ({percentage:.1f}%)")

        monthly = self.df.assign(Month=self.df["Date"].dt.to_period("M")).groupby("Month")["Amount"].sum()
        if not monthly.empty:
            print("\nMonthly Spending:")
            print(monthly.to_string())
            print(f"Average Monthly Spending: {monthly.mean():.2f}")

    def filter_expenses(self, category=None, min_amount=None, start_date=None, end_date=None):
        """Filter records by category, minimum amount, and optional date range."""
        filtered = self.df.copy()

        if category:
            filtered = filtered[
                filtered["Category"].str.casefold() == category.strip().casefold()
            ]
        if min_amount is not None:
            filtered = filtered[filtered["Amount"] >= float(min_amount)]
        try:
            if start_date:
                filtered = filtered[filtered["Date"] >= self._parse_date(start_date)]
            if end_date:
                filtered = filtered[filtered["Date"] <= self._parse_date(end_date)]
        except (ValueError, TypeError):
            print("Error: Enter dates in YYYY-MM-DD format.")
            return

        print("\n--- FILTERED RESULTS ---")
        if filtered.empty:
            print("No matching expenses found.")
        else:
            print(filtered.to_string(index=False))

    def generate_report(self):
        """Create a four-chart expense report."""
        if self.df.empty:
            print("No data available to plot charts.")
            return

        sns.set_theme(style="whitegrid")
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle("Smart Expense Tracker Analytics", fontsize=16)

        category_data = self.df.groupby("Category", as_index=False)["Amount"].sum()
        sns.barplot(data=category_data, x="Category", y="Amount",
                    ax=axes[0, 0], color="steelblue")
        axes[0, 0].set_title("Total Expenses by Category")
        axes[0, 0].tick_params(axis="x", rotation=25)

        time_data = self.df.groupby("Date", as_index=False)["Amount"].sum().sort_values("Date")
        sns.lineplot(data=time_data, x="Date", y="Amount",
                     ax=axes[0, 1], marker="o", color="green")
        axes[0, 1].set_title("Spending Trends Over Time")
        axes[0, 1].tick_params(axis="x", rotation=45)

        category_totals = self.df.groupby("Category")["Amount"].sum()
        axes[1, 0].pie(category_totals, labels=category_totals.index,
                       autopct="%1.1f%%", startangle=140)
        axes[1, 0].set_title("Spending Distribution by Category")

        sns.histplot(data=self.df, x="Amount", kde=len(self.df) > 1,
                     ax=axes[1, 1], color="purple", bins=5)
        axes[1, 1].set_title("Frequency of Expense Amounts")

        plt.tight_layout()
        plt.show()


def main():
    tracker = ExpenseTracker("expenses.csv")

    while True:
        print("\n====== SMART EXPENSE TRACKER ======")
        print("1. Add New Expense")
        print("2. View Expense Summary")
        print("3. Filter Expenses")
        print("4. Generate Visual Charts")
        print("5. Exit")

        choice = input("Enter choice (1-5): ")

        if choice == "1":
            date = input("Enter date (YYYY-MM-DD): ").strip()
            amount = input("Enter amount: ").strip()
            print("Categories:", ", ".join(ExpenseTracker.get_valid_categories()))
            category = input("Enter category: ").strip()
            description = input("Enter description: ").strip()
            tracker.add_expense(date, amount, category, description)

        elif choice == "2":
            tracker.get_summary()

        elif choice == "3":
            category = input("Enter category to filter (or Enter to skip): ").strip()
            amount_text = input("Enter minimum amount (or Enter to skip): ").strip()
            start_date = input("Start date YYYY-MM-DD (or Enter to skip): ").strip()
            end_date = input("End date YYYY-MM-DD (or Enter to skip): ").strip()
            try:
                min_amount = float(amount_text) if amount_text else None
                if min_amount is not None and min_amount < 0:
                    print("Minimum amount cannot be negative.")
                    continue
                if start_date and end_date and pd.to_datetime(start_date) > pd.to_datetime(end_date):
                    print("Start date cannot be after end date.")
                    continue
                tracker.filter_expenses(
                    category=category or None,
                    min_amount=min_amount,
                    start_date=start_date or None,
                    end_date=end_date or None
                )
            except ValueError:
                print("Error: Enter a valid minimum amount and/or date.")

        elif choice == "4":
            tracker.generate_report()

        elif choice == "5":
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()





       