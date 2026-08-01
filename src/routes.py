from fastapi import APIRouter, HTTPException

from src.models import ExpenseCreate
from src.storage import (
    get_all_expenses,
    add_expense,
    delete_expense,
    filter_by_category,
    calculate_total,
    calculate_category_total,
    monthly_summary,
)
from src.utils import generate_expense_id

router = APIRouter()


@router.get("/health", tags=["Health"])
def health_check():
    """Check whether the API is running."""
    return {"status": "API is running successfully"}


@router.post("/expenses", tags=["Expenses"], status_code=201)
def create_expense(expense: ExpenseCreate):
    """Create a new expense."""

    new_expense = {
        "id": generate_expense_id(),
        "title": expense.title,
        "amount": expense.amount,
        "category": expense.category,
        "date": str(expense.date),
    }

    saved_expense = add_expense(new_expense)

    return {
        "success": True,
        "message": "Expense added successfully",
        "data": saved_expense,
    }


@router.get("/expenses", tags=["Expenses"])
def get_expenses():
    """Retrieve all stored expenses."""

    expenses = get_all_expenses()

    return {
        "success": True,
        "count": len(expenses),
        "data": expenses,
    }


@router.get("/expenses/category/{category}", tags=["Expenses"])
def get_expenses_by_category(category: str):
    """Filter expenses by category."""

    expenses = filter_by_category(category)

    return {
        "success": True,
        "category": category,
        "count": len(expenses),
        "data": expenses,
    }


@router.get("/expenses/total", tags=["Statistics"])
def get_total_expenses():
    """Calculate the total amount of all expenses."""

    return {
        "success": True,
        "data": {
            "total_expenses": calculate_total()
        },
    }


@router.get("/expenses/total/{category}", tags=["Statistics"])
def get_category_total(category: str):
    """Calculate the total expenses for a specific category."""

    return {
        "success": True,
        "data": {
            "category": category,
            "total": calculate_category_total(category),
        },
    }


@router.delete("/expenses/{expense_id}", tags=["Expenses"])
def remove_expense(expense_id: str):
    """Delete an expense by its unique ID."""

    deleted = delete_expense(expense_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Expense not found",
        )

    return {
        "success": True,
        "message": "Expense deleted successfully",
    }


@router.get("/expenses/monthly-summary", tags=["Statistics"])
def get_monthly_summary():
    """Generate a summary of expenses grouped by month."""

    return {
        "success": True,
        "data": monthly_summary(),
    }