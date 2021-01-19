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
        title='some cool title',
        amount='some cool amount',
        created_at='Super cool date',
        tags='some cool tags'
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
        title='some cool title',
        amount='some cool amount',
        created_at='Super cool date',
        tags='some cool tags'
    ).execute()
    
    expense_id = len(Expense.ListAll())
    edit = EditExpenseCommand(
        id=expense_id,
        title='some fdsaf title',
        amount='some dsaf amount',
        created_at='Super cofdaol date',
        tags='some fda tags'
    )
    expense_edit = edit.execute()

    db_expense = Expense.GetExpenseByID(expense_id)

    assert db_expense.title == expense_edit.title
    assert db_expense.amount == expense_edit.amount
    assert db_expense.created_at == expense_edit.created_at
    assert db_expense.tags == expense_edit.tags