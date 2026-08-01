from fastapi import FastAPI
from src.routes import router

app = FastAPI(
    title="Smart Expense Tracker API",
    description="""
A RESTful API for managing personal expenses.

## Features
- Add an expense
- View all expenses
- Filter expenses by category
- Calculate total expenses
- Calculate category-wise totals
- Delete an expense
- Monthly expense summary
""",
    version="1.0.0",
    contact={
        "name": "Bismillah Ansari",
        "email": "bismiansari157@gmail.com"  
    },
    license_info={
        "name": "MIT License",
    },
)

app.include_router(router)


@app.get("/", tags=["Home"])
def root():
    """Welcome endpoint."""
    return {
        "message": "Welcome to Smart Expense Tracker API",
        "docs": "/docs"
    }