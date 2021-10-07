from datetime import timedelta
import expenses

import os

from flask import Flask, jsonify, request, render_template, redirect, session, url_for, flash
from werkzeug.datastructures import ContentRange

from expenses.commands import CreateExpenseCommand, EditExpenseCommand, CreateNewUser
from expenses.queries import ListExpensesQuery, GetExpenseByIDQuery, GetUserByEmailQuery

from flask_sqlalchemy import SQLAlchemy

from pydantic import ValidationError

from expenses.models import NotFound, Users

"""Create and configure an instance of the Flask application."""
app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)

# # set config
# app_settings = os.getenv('APP_SETTINGS')  # new
# app.config.from_object(app_settings) 

@app.errorhandler(ValidationError)
def handle_validation_exception(error):
    response = jsonify(error.errors())
    response.status_code = 400
    return response

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["email"]
        session["email"] = user
        
        found_user = GetUserByEmailQuery(email=user).execute()

        if found_user is NotFound:
            return redirect(url_for("registration"))
        return redirect(url_for("user"))
       
        
    else:
        if "user" in session:
            flash("Already Logged in!")
            return redirect(url_for("user"))
        
        return render_template("login.html")

@app.route("/registration", methods=["POST", "GET"])
def registration():
    if request.method == "POST":
        email = request.form['email']
        check_email_registered = GetUserByEmailQuery(email=email).execute()
        if check_email_registered is NotFound:
            CreateNewUser(name=request.form['name'],
                            email=request.form['email'],
                            password=request.form['password'],
            ).execute()
            return redirect(url_for("login"))
        else:
            flash('That email already exists!')
            return render_template("registration.html")
    else:
        return render_template("registration.html")


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
    print('hello', request.json)
    cmd = CreateExpenseCommand(
        **request.json
    )
    
    return jsonify(cmd.execute().dict())

@app.route('/edit-expense/<expense_id>/', methods=['PUT'])
def edit_expense(expense_id):
    cmd = EditExpenseCommand(
        **request.json
    )
    return jsonify(cmd.execute().dict())

@app.route('/expense/<expense_id>/', methods=['GET'])
def get_expense(expense_id, email):
    query = GetExpenseByIDQuery(
        id=expense_id,
        email=email
    )
    return jsonify(query.execute().dict())

@app.route('/expense-list/', methods=['GET'])
def list_expenses():
    query = ListExpensesQuery(**request.json)
    records = [record.dict() for record in query.execute()]
    return jsonify(records)
