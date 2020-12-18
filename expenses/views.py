from flask import render_template

from expenses.commands import CreateExpenseCommand, EditExpenseCommand
from expenses.queries import ListExpensesQuery, GetExpenseByIDQuery

def views(app):
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

    @app.route("/admin/dashboard")
    def admin_dashboard():
        return render_template("admin/dashboard.html")

    @app.route("/jinja")
    def jinja():

        my_name = 'Andrew'

        return render_template("public/jinja.html", my_name=my_name)