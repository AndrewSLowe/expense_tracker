from pydantic import EmailStr, Field

import pytest
from expenses.models import Expense, Users
from expenses.commands import CreateExpenseCommand, EditExpenseCommand, CreateNewUser

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
        tags='dairy',
        email='andrew@gmail.com'
    )

    expense = cmd.execute()

    db_expense = Expense.GetExpenseByID(expense.id, expense.email)

    assert db_expense.id == expense.id
    assert db_expense.title == expense.title
    assert db_expense.amount == expense.amount
    assert db_expense.created_at == expense.created_at
    assert db_expense.tags == expense.tags
    assert db_expense.email == expense.email

def test_edit_expense():
    """
    GIVEN EditExpenseCommand with a valid properties title, amount, created_at and content
    WHEN the execute method is called
    THEN a new Expense must exist in the database with the same attributes
    """
    expense = CreateExpenseCommand(
        title='New Expense',
        amount=12.0,
        created_at='12/08/1994',
        tags='dairy',
        email='andrewwe@gmail.com'
    ).execute()

    edit_expense = EditExpenseCommand(
        id=expense.id,
        title='New Expense edit',
        amount=24.0,
        created_at='12/08/1995',
        tags='dairyyyy',
        email=expense.email
    ).execute()

    edit_expense_check = Expense.GetExpenseByID(id=expense.id, email=expense.email)

    assert edit_expense_check.id == edit_expense.id
    assert edit_expense_check.title == edit_expense.title
    assert edit_expense_check.amount == edit_expense.amount
    assert edit_expense_check.created_at == edit_expense.created_at
    assert edit_expense_check.tags == edit_expense.tags
    assert edit_expense_check.email == edit_expense.email

def test_create_user():
    """
    GIVEN CreateNewUser with valid properties: name, password, email
    WHEN the execute method is called
    THEN a new User must exist in the database with the same attributes
    """
    cmd = CreateNewUser(
        name='Andrew',
        password='secret_password',
        email='andy@gmail.com'
    )
    
    user = cmd.execute()
    print(user.email)
    db_user = Users.GetUserByEmail(user.email)

    assert db_user.name == user.name
    assert db_user.password == user.password
    assert db_user.email == user.email
    assert db_user.created_at == user.created_at
    assert db_user.active == user.active
    assert db_user.email == user.email