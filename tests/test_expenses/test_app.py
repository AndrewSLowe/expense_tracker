import json
import pathlib

import pytest
from jsonschema import validate, RefResolver

from expenses.app import app
from expenses.models import Expense

@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

def validate_payload(payload, schema_name):
    """
    Validate payload with selected schema
    """
    schemas_dir = str(
        f'{pathlib.Path(__file__).parent.absolute()}/schemas'
    )
    schema = json.loads(pathlib.Path(f'{schemas_dir}/{schema_name}').read_text())
    validate(
        payload,
        schema,
        resolver=RefResolver(
            'file://' + str(pathlib.Path(f'{schemas_dir}/{schema_name}').absolute()),
            schema # it's used to resolve file: inside shemas correctly
        )
    )

def test_create_expense(client):
    """
    GIVEN ID of expense stored in the database
    WHEN endpoint /create-expense/ is called
    THEN it should return Expense in json format matching schema
    """
    data = {
        'title':'some cool title',
        'amount':'some cool amount',
        'created_at':'Super cool date',
        'tags':'some cool tags'
    }

    response = client.post(
        '/create-expense/',
        data=json.dumps(
            data
        ),
        content_type='application/json'
    )

    validate_payload(response.json, 'Expense.json')

def test_list_expenses(client):
    """
    GIVEN expenses stored in the database
    WHEN endpoint /expense-list/ is called
    THEN it should return list of Expense in json format matching schema
    """
    Expense(
        title='New Expense',
        amount='cool amount',
        created_at='neat date',
        tags='many awesome cool tags'
    ).AddExpense()
    response = client.get(
        '/expense-list/',
        content_type='application/json',
    )

    validate_payload(response.json, 'ExpenseList.json')