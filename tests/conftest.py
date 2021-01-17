# Run by default after each test.
import os
import tempfile
import random

import pytest

from expenses.models import Expense

@pytest.fixture(autouse=True)    # autouse flag set to True: automatically used before and after each test
def database():
    _, file_name = tempfile.mkstemp()
    os.environ['DATABASE_NAME'] = file_name
    Expense.create_table(database_name=file_name)
    yield
    os.unlink(file_name)