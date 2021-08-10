from expenses.models import Expense
from expenses.queries import ListExpensesQuery, GetExpenseByIDQuery

def test_list_expenses():
    """
    GIVEN 2 expenses stored in the database
    WHEN the execute method is called
    THEN it should return 2 expenses
    """
    Expense(
        title='New Expense',
        amount=12.0,
        created_at='12/08/1994',
        tags='dairy'
    ).AddExpense()

    Expense(
        title='New Expense',
        amount=12.0,
        created_at='12/08/1994',
        tags='dairy'
    ).AddExpense()

    query = ListExpensesQuery()

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
        tags='dairy'
    ).AddExpense()

    expense_id = len(ListExpensesQuery().execute())

    query = GetExpenseByIDQuery(
        id=expense_id
    )

    assert query.execute().title == expense.title
    assert query.execute().amount == expense.amount
    assert query.execute().created_at == expense.created_at
    assert query.execute().tags == expense.tags