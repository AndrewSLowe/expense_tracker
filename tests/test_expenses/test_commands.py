import pytest
from expenses.models import Expense
from expenses.commands import CreateExpenseCommand, EditExpenseCommand

def test_create_expense():
    """
    GIVEN CreateExpenseCommand with a valid properties title, amount, created_at and content
    WHEN the execute method is called
    THEN a new Expense must exist in the database with the same attributes
    """
    cmd = CreateExpenseCommand(
        title='New Expense',
        amount=12.0,
        created_at='12/08/1994',
        tags='dairy'
    )

    expense = cmd.execute()

    expense_id = len(Expense.ListAll())
    db_expense = Expense.GetExpenseByID(expense_id)

    assert db_expense.title == expense.title
    assert db_expense.amount == expense.amount
    assert db_expense.created_at == expense.created_at
    assert db_expense.tags == expense.tags

def test_edit_expense():
    """
    GIVEN EditExpenseCommand with a valid properties title, amount, created_at and content
    WHEN the execute method is called
    THEN a new Expense must exist in the database with the same attributes
    """
    CreateExpenseCommand(
        title='New Expense',
        amount=12.0,
        created_at='12/08/1994',
        tags='dairy'
    ).execute()
    
    expense_id = len(Expense.ListAll())
    edit = EditExpenseCommand(
        id=expense_id,
        title='New Expense edit',
        amount=24.0,
        created_at='12/08/1995',
        tags='dairyyyy'
    )
    expense_edit = edit.execute()

    db_expense = Expense.GetExpenseByID(expense_id)

    assert db_expense.title == expense_edit.title
    assert db_expense.amount == expense_edit.amount
    assert db_expense.created_at == expense_edit.created_at
    assert db_expense.tags == expense_edit.tags