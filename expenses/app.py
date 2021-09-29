from datetime import timedelta
import expenses

import os

from flask import Flask, jsonify, request, render_template, redirect, session, url_for, flash
from werkzeug.datastructures import ContentRange

from expenses.commands import CreateExpenseCommand, EditExpenseCommand
from expenses.queries import ListExpensesQuery, GetExpenseByIDQuery

from flask_sqlalchemy import SQLAlchemy

from pydantic import ValidationError

from expenses.models import Users


"""Create and configure an instance of the Flask application."""
app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)

# set config
app_settings = os.getenv('APP_SETTINGS')  # new
app.config.from_object(app_settings) 

@app.errorhandler(ValidationError)
def handle_validation_exception(error):
    response = jsonify(error.errors())
    response.status_code = 400
    return response

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        
        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email
            
        else:
            usr = Users(user, "")
            usr.AddUser()
        flash("Login successful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged in!")
            return redirect(url_for("user"))
        
        return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved!")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html", email=email)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    flash(f"You have been logged out!", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))



@app.route('/create-expense/', methods=['POST', 'GET'])
def create_expense():

    cmd = CreateExpenseCommand(
        **request.json
    )
    
    return jsonify(cmd.execute().dict())
    # return render_template('index.html', content="Testing ")

@app.route('/edit-expense/<expense_id>/', methods=['PUT'])
def edit_expense(expense_id):
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

if __name__ == '__main__':
    db.create_all()
    app.run()