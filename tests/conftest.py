# Run by default after each test.
import os

import pytest

from expenses.models import Expense, Users

@pytest.fixture(scope='function', autouse=True)    # autouse flag set to True: automatically used before and after each test
def clear_tables():
    test_db = os.environ.get('DATABASE_TEST_URL')
    os.environ['DATABASE_NAME'] = test_db
    yield
    Expense.drop_table(database_name=test_db)
    Users.drop_table(database_name=test_db)
    os.environ.pop('DATABASE_NAME', None)