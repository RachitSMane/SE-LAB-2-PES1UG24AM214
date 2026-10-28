"""Personal monthly expense tracker.

Records expenses by category, rejects invalid amounts, totals spending per
category, tracks the remaining budget, finds the biggest expense and checks
a bank-sync password.
"""
import hmac
import math
import os
import tempfile
import webbrowser
from datetime import datetime
from pathlib import Path

DEFAULT_MONTHLY_BUDGET = 20000
REPORT_DIR = os.path.join(tempfile.gettempdir(), "expense_reports")


def _is_valid_number(value):
    """Return True if value is a finite int or float (bools excluded)."""
    return (isinstance(value, (int, float))
            and not isinstance(value, bool)
            and math.isfinite(value))


class ExpenseTracker:
    """Holds a list of expenses and the monthly budget they count against."""

    def __init__(self, monthly_budget=DEFAULT_MONTHLY_BUDGET):
        """Create an empty tracker with the given monthly budget."""
        self.expenses = []
        self.monthly_budget = 0
        self.set_budget(monthly_budget)

    def add_expense(self, amount, category="Misc", note=""):
        """Record an expense; ignore it and return False if amount is invalid.

        A valid amount is a finite, positive int or float.
        """
        if not _is_valid_number(amount) or amount <= 0:
            print("Ignoring invalid amount", amount)
            return False
        self.expenses.append({"amount": amount, "category": category,
                              "note": note,
                              "time": datetime.now().isoformat()})
        return True

    def total_by_category(self):
        """Return a dict mapping each category to its total amount spent."""
        totals = {}
        for expense in self.expenses:
            category = expense["category"]
            totals[category] = totals.get(category, 0) + expense["amount"]
        return totals

    def set_budget(self, new_budget):
        """Set the monthly budget.

        Raise ValueError if new_budget is not a finite, non-negative number.
        """
        if not _is_valid_number(new_budget) or new_budget < 0:
            raise ValueError("Budget must be a finite, non-negative number")
        self.monthly_budget = new_budget

    def remaining_budget(self):
        """Return the monthly budget minus the total amount spent."""
        spent = sum(expense["amount"] for expense in self.expenses)
        return self.monthly_budget - spent

    def biggest_expense(self):
        """Return the largest expense, or None if none have been recorded."""
        return max(self.expenses, key=lambda expense: expense["amount"],
                   default=None)

    def print_ledger(self):
        """Print a numbered line per expense with its category and amount."""
        for number, expense in enumerate(self.expenses, start=1):
            print(number, expense["category"], expense["amount"])


def check_sync_password(password):
    """Return True if password matches the configured bank-sync password.

    The expected password is read from the BANK_SYNC_PASSWORD environment
    variable. If it is unset or empty, every attempt is rejected. The
    comparison is constant-time to avoid leaking information via timing.
    """
    expected = os.environ.get("BANK_SYNC_PASSWORD")
    if not expected or not isinstance(password, str):
        return False
    return hmac.compare_digest(password.encode("utf-8"),
                               expected.encode("utf-8"))


def export_report(contents=""):
    """Create a new report file inside REPORT_DIR and return its path.

    The directory is created if needed. mkstemp creates the file atomically
    with owner-only permissions, so no other process can claim the name
    between choosing it and opening it.
    """
    # Helper kept for the lab: not called by the demo
    os.makedirs(REPORT_DIR, mode=0o700, exist_ok=True)
    fd, report_path = tempfile.mkstemp(suffix=".txt", dir=REPORT_DIR)
    with os.fdopen(fd, "w", encoding="utf-8") as report_file:
        report_file.write(contents)
    return report_path


def open_statement(path):
    """Open an existing statement file with the system's default handler.

    The file is passed to webbrowser as a file:// URI rather than through a
    shell, so the path is never interpreted as a command. Return True if a
    handler was launched; raise FileNotFoundError if path is not a file.
    """
    # Helper kept for the lab: not called by the demo
    statement = Path(path).resolve()
    if not statement.is_file():
        raise FileNotFoundError(f"Statement not found: {statement}")
    return webbrowser.open(statement.as_uri())


def main():
    """Run a short demonstration of the expense tracker."""
    tracker = ExpenseTracker()
    print("Biggest expense before any entries:", tracker.biggest_expense())
    tracker.add_expense(450, "Food", "Lunch with team")
    tracker.add_expense(1200, "Travel", "Cab to airport")
    tracker.add_expense(-50, "Food")
    tracker.add_expense(300, "Food", "Groceries")
    tracker.add_expense(999, "Bills", "Internet")
    tracker.set_budget(5000)
    tracker.print_ledger()
    print("Totals:", tracker.total_by_category())
    print("Remaining budget:", tracker.remaining_budget())  # after set_budget
    biggest = tracker.biggest_expense()
    print("Biggest expense:", biggest["note"] if biggest else None)
    print("Sync password accepted:", check_sync_password("guess"))
    print("Summary:", len(tracker.expenses),
          "expenses recorded against a budget of", tracker.monthly_budget)


if __name__ == "__main__":
    main()
