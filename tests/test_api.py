from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)



def test_home():
    """Verify the home endpoint returns API information."""
    response = client.get("/")

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Welcome to Smart Expense Tracker API"
    assert body["docs"] == "/docs"


def test_health():
    """Verify API health endpoint."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "API is running successfully"


def test_add_expense():
    """Verify a new expense can be added."""
    expense = {
        "title": "Book",
        "amount": 500,
        "category": "Education",
        "date": "2026-08-01"
    }

    response = client.post("/expenses", json=expense)

    assert response.status_code == 201

    body = response.json()

    assert body["success"] is True
    assert body["message"] == "Expense added successfully"
    assert body["data"]["title"] == "Book"


def test_get_all_expenses():
    """Verify all expenses can be retrieved.""" 
    response = client.get("/expenses")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert "count" in body
    assert isinstance(body["data"], list)


def test_filter_category():
    response = client.get("/expenses/category/Education")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["category"] == "Education"


def test_total_expenses():
    response = client.get("/expenses/total")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert "total_expenses" in body["data"]


def test_category_total():
    response = client.get("/expenses/total/Education")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["data"]["category"] == "Education"


def test_monthly_summary():
    response = client.get("/expenses/monthly-summary")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert isinstance(body["data"], dict)


def test_delete_expense():
    """Verify an existing expense can be deleted."""

    expense = {
        "title": "Laptop",
        "amount": 50000,
        "category": "Electronics",
        "date": "2026-08-01",
    }

    create_response = client.post("/expenses", json=expense)

    expense_id = create_response.json()["data"]["id"]

    delete_response = client.delete(f"/expenses/{expense_id}")

    assert delete_response.status_code == 200

    body = delete_response.json()

    assert body["success"] is True
    assert body["message"] == "Expense deleted successfully"

    

def test_delete_invalid_expense():
    response = client.delete("/expenses/invalid-id")

    assert response.status_code == 404