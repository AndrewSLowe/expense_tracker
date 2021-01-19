import json
import pathlib
import requests

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

def test_edit_expense(client):
    """
    GIVEN ID of expense stored in the database
    WHEN endpoint /create-expense/ is called
    THEN it should return Expense in json format matching schema
    """
    data = {
        'id':1,
        'title':'some cool title',
        'amount':'some cool amount',
        'created_at':'Super cool date',
        'tags':'some cool tags'
    }

    response = client.put(
        '/edit-expense/',
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

@pytest.mark.parametrize(
    'data',
    [
        {
            'title': 'an item',
            'amount': 'an amount',
            'created_at': 'a date',
        },
        {
            'title': 'an item',
            'amount': 'an amount',
        },
        {
            'title': 'an item',
            'amount': None,
            'created_at': 'a date',
            'tags': 'some tags'
        },
        {
            'title': 'an item',
            'amount': None,
            'created_at': 'date',
            'tags': None
        },
        {
            'title': 'an item',
            'amount': 'an amount',
            'created_at': 'date',
            'tags': None
        },
    ]
)

def test_create_expense_bad_request(client, data):
    """
    GIVEN request data with invalid values or missing attributes
    WHEN enpoint /create-article/ is called
    THEN it should return status 400 and JSON body
    """
    response = client.post(
        '/create-expense/',
        data=json.dumps(
            data
        ),
        content_type='application/json'
    )

    assert response.status_code == 400
    assert response.json is not None

@pytest.mark.e2e
def test_create_list_get(client):
    requests.post(
        'http://localhost:5000/create-expense/',
        json={
            'title': 'an item',
            'amount': 14,
            'created_at': 'date',
            'tags': 'hello world'
        },
    )
    response = requests.get(
        'http://localhost:5000/expense-list/',
    )
    expenses = response.json()

    response = requests.get(
        f'http://localhost:5000/expense/{expenses[0]["id"]}/',
    )

    assert response.status_code == 200