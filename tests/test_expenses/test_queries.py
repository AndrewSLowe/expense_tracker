from expenses.models import Expense, Users
from expenses.queries import ListExpensesQuery, GetExpenseByIDQuery, GetUserByEmailQuery

def test_list_expenses():
    """
    GIVEN 2 expenses stored in the database
    WHEN the execute method is called
    THEN it should return 2 expenses
    """
    Expense(
        title='New Egdsahggewxpense',
        amount=12.0,
        created_at='12/08/1994',
        tags='daifdsafdsary',
        email='dafdasg@gmail.com'
    ).AddExpense()

    expense = Expense(
        title='New Expense',
        amount=12.0,
        created_at='12/08/1994',
        tags='dairy',
        email='dafdasg@gmail.com'
    ).AddExpense()

    query = ListExpensesQuery(email=expense.email)

    assert len(query.execute()) == 2

def test_get_expense_by_id():
    """
    GIVEN ID of article stored in the database
    WHEN the execute method is called GetExpenseByIDQuery with id set
    THEN it should return the expense with the same id
    """
    expense = Expense(
        title='New Expense',
        amount=12.0,
        created_at='12/08/1994',
        tags='dairy',
        email='andrew@gmail.com'
    ).AddExpense()

    query = GetExpenseByIDQuery(
        id=expense.id,
        email=expense.email
    ).execute()

    assert query.title == expense.title
    assert query.amount == expense.amount
    assert query.created_at == expense.created_at
    assert query.tags == expense.tags

def test_get_user_by_email():
    """
    GIVEN ID of article stored in the database
    WHEN the execute method is called GetExpenseByIDQuery with id set
    THEN it should return the expense with the same id
    """
    expense = Users(
        name='some guy',
        password='super secret pass',
        email='andrew@gmail.com'
    ).AddUser()

    query = GetUserByEmailQuery(
        email=expense.email
    ).execute()

    assert query.name == expense.name
    assert query.password == expense.password
    assert query.email == expense.email
    assert query.created_at == expense.created_at
    assert query.active == expense.active