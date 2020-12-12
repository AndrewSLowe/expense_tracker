import pytest

from expenses.models import Expense
from expenses.commands import CreateExpenseCommand

def test_create_expense():
    """
    GIVEN CreateExpenseCommand with a valid properties title, amount, created_at and content
    WHEN the execute method is called
    THEN a new Expense must exist in the database with the same attributes
    """
    cmd = CreateExpenseCommand(
        title='some cool title',
        amount='some cool amount',
        created_at='Super cool date',
        tags='some cool tags'
    )

    expense = cmd.execute()

    db_expense = Expense.GetByID(expense.id)

    assert db_expense.id == expense.id
    assert db_expense.title == expense.title
    assert db_expense.amount == expense.amount
    assert db_expense.created_at == expense.created_at
    assert db_expense.tags == expense.tags