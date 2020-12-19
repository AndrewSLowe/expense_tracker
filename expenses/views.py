from flask import render_template, request, redirect

from expenses.commands import CreateExpenseCommand, EditExpenseCommand
from expenses.queries import ListExpensesQuery, GetExpenseByIDQuery

def views(app):
    @app.route('/')
    def root():
        return render_template('public/index.html', title='Create Expense')

    @app.route("/sign-up", methods=["GET", "POST"])
    def sign_up():

        if request.method == "POST":

            req = request.form

            missing = list()

            for k, v in req.items():
                if v == "":
                    missing.append(k)

            if missing:
                feedback = f"Missing fields for {', '.join(missing)}"
                return render_template("public/sign_up.html", feedback=feedback)

            return redirect(request.url)

        return render_template("public/sign_up.html")

    users = {
        "funguy": {
            'name': 'Andrew Lowe',
            'bio': 'tryna save some money',
            'twitter_handle': '@andrewloweGR'
        }

    }

    @app.route('/profile/<username>')
    def profile(username):
        
        user = None
        if username in users:
            user = users[username]

        return render_template("public/profile.html", user=user)

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

        my_name = 'poopy'

        age = 25

        langs = ['python', 'js', 'C']

        friends = {
            'tom': 20,
            'sally': 25,
            'Alice': 16
        }

        return render_template("public/jinja.html", my_name=my_name)