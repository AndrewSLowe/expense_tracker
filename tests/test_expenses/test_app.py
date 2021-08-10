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
        'amount':12.0,
        'created_at':'12/08/1994',
        'tags':'dairy'
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
        'amount':12.0,
        'created_at':'12/08/1994',
        'tags':'dairy'
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
        amount=12.0,
        created_at='12/08/1994',
        tags='dairy'
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
            'amount': 12.0,
            'created_at': '12/08/1994'
        },
        {
            'title': 'an item',
            'amount': 12.0
        },
        {
            'title': 'an item',
            'amount': None,
            'created_at': '12/08/1994',
            'tags': 'dairy'
        },
        {
            'title': 'an item',
            'amount': None,
            'created_at': '12/08/1994',
            'tags': None
        },
        {
            'title': 'an item',
            'amount': 12.0,
            'created_at': '12/08/1994',
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
            'title': 'item',
            'amount': 14,
            'created_at': '12/08/1994',
            'tags': 'some cool tags'
        },
    )
    response = requests.get(
        'http://localhost:5000/expense-list/',
    )
    expenses = len(response.json())
    response = requests.get(
        f'http://localhost:5000/expense/{expenses}/'
    )

    assert response.status_code == 200