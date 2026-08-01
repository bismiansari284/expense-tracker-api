import uuid


def generate_expense_id() -> str:
    """Generate a unique expense ID."""
    return str(uuid.uuid4())