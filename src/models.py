from datetime import date
from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    """Model used to create a new expense."""
    title: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=50)
    date: date


class Expense(ExpenseCreate):
    """Complete expense model including its unique identifier."""
    id: str