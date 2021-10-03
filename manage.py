
from flask.cli import FlaskGroup

from expenses import app
from expenses.models import Expense, Users

cli = FlaskGroup(app)


if __name__ == '__main__':
    Expense.create_table()
    Users.create_table()
    cli()