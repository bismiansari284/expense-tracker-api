import json
from pathlib import Path
from typing import List
from collections import defaultdict

DATA_FILE = Path(__file__).parent / "expenses.json"


def load_expenses() -> List[dict]:
    """Load all expenses from the JSON file."""
    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_expenses(expenses: List[dict]) -> None:
    """Save all expenses to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4)


def get_all_expenses() -> List[dict]:
    """Retrieve all stored expenses."""
    return load_expenses()


def add_expense(expense: dict) -> dict:
    """Add a new expense."""
    expenses = load_expenses()
    expenses.append(expense)
    save_expenses(expenses)
    return expense


def delete_expense(expense_id: str) -> bool:
    """Delete an expense by its ID."""
    expenses = load_expenses()

    updated = [expense for expense in expenses if expense["id"] != expense_id]

    if len(updated) == len(expenses):
        return False

    save_expenses(updated)
    return True


def filter_by_category(category: str) -> List[dict]:
    """Retrieve expenses belonging to a category."""
    expenses = load_expenses()

    return [
        expense
        for expense in expenses
        if expense["category"].lower() == category.lower()
    ]


def calculate_total() -> float:
    """Calculate total expenses."""
    expenses = load_expenses()
    return sum(expense["amount"] for expense in expenses)


def calculate_category_total(category: str) -> float:
    """Calculate total expenses for a category."""
    expenses = load_expenses()

    return sum(
        expense["amount"]
        for expense in expenses
        if expense["category"].lower() == category.lower()
    )


def monthly_summary() -> dict[str, float]:
    """Generate monthly expense totals."""
    expenses = load_expenses()

    summary: dict[str, float] = defaultdict(float)

    for expense in expenses:
        # Extract year and month (YYYY-MM)
        month = expense["date"][:7]
        summary[month] += expense["amount"]

    return dict(summary)
