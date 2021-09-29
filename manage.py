
from flask.cli import FlaskGroup

from expenses import app
from expenses.models import Expense, Users

cli = FlaskGroup(app)


if __name__ == '__main__':
    Expense.create_table()
    Expense(
            title='Marianos', 
            amount=23.2, 
            created_at='12/01/1993',
            tags='groc',
            email='andrewstevenlowe@gmail.com').AddExpense()
    Expense(
        title='fdsafdsaf', 
        amount=23.2, 
        created_at='12/01/1993',
        tags='groc',
        email='andrewstevenlowe@gmail.com'
    ).EditExpense('19fc7827-a112-42ae-9c43-2810441638c2')
    Expense.GetExpenseByID('19fc7827-a112-42ae-9c43-2810441638c2', 'andrewstevenlowe@gmail.com')
    Expense.ListAll('andrewstevenlowe@gmail.com')

    Users.create_table()
    Users(
            name='Andrew Lowe',
            email='andrewstevenlowe@gmail.com').AddUser()
    cli()