# Run by default after each test.
import os
import tempfile
import random

import pytest

from expenses.models import Expense, Users

@pytest.fixture(autouse=True)    # autouse flag set to True: automatically used before and after each test
def database():
    Expense.drop_table()
    Expense.create_table()
    Users.drop_table()
    Users.create_table()
    yield