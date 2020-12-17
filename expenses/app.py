from flask import Flask, jsonify, request, render_template

from expenses.commands import CreateExpenseCommand, EditExpenseCommand
from expenses.queries import ListExpensesQuery, GetExpenseByIDQuery
from expenses.models import Expense
from pydantic import ValidationError

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    
    # initialize db
    Expense.create_table()

    @app.errorhandler(ValidationError)
    def handle_validation_exception(error):
        response = jsonify(error.errors())
        response.status_code = 400
        return response

    @app.route('/')
    def root():
        return render_template('public/index.html', title='Home')

    @app.route("/about")
    def about():
        return """
        <h1 style='color: red;'>I'm a red H1 heading!</h1>
        <p>This is a lovely little paragraph</p>
        <code>Flask is <em>awesome</em></code>
        """

    @app.route('/create-expense/', methods=['POST'])
    def create_expense():
        cmd = CreateExpenseCommand(
            **request.json
        )
        return jsonify(cmd.execute().dict())

    @app.route('/edit-expense/', methods=['PUT'])
    def edit_expense():
        cmd = EditExpenseCommand(
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
    
    return app

if __name__ == '__main__':
    create_app()