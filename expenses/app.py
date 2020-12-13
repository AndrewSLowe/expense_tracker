from flask import Flask, jsonify, request

from expenses.commands import CreateExpenseCommand, EditExpenseCommand
from expenses.queries import ListExpensesQuery, GetExpenseByIDQuery

app = Flask(__name__)

@app.route('/create-expense/', methods=['POST'])
def create_expense():
    cmd = CreateExpenseCommand(
        **request.json
    )
    return jsonify(cmd.execute().dict())

@app.route('/expense/<expense_id>/', methods=['GET'])
def get_expense(expense_id):
    query = GetExpenseByIDQuery(
        id=expense_id
    )
    return jsonify(query.execute().dict())

@app.route('/expense-list/', methods=['GET'])
def list_expenses():
    query = ListExpensesQuery()
    records = [record.dict() for record in query.execute()]
    return jsonify(records)

if __name__ == '__main__':
    app.run()