import os

from flask import Flask, flash, session, jsonify, redirect, url_for, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from pprint import pprint
from dbsetup import createUsers, createBooks, createReviews
from importBooks import importBooks
from models import User

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
else:
    print("Database detected, running application")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.urandom(64)

Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Initialize the databse

userInit = createUsers()
booksInit = createBooks()
reviewsInit = createReviews()

# Import the books
importBooks()

@app.route("/")
def index():

    if 'logged_in' not in session:
        session['logged_in'] = False
        return redirect(url_for('login'))

    if session['logged_in']:
            return '<h1>You are logged in!</h1>'
    else:
        session.pop('logged_in', None)
        return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        userEmail = request.form.get("email")
        userPassword = request.form.get("password")
        userID = db.execute("SELECT id FROM users WHERE email = :email AND password = :password",
            {"email": userEmail, "password": userPassword}).fetchone()
        if userID is None:
            return "Wrong credentials"
        else:
            session['logged_in'] = True
            flash('Success')
            return render_template("login.html", message="You are now logged in")

@app.route("/logout")
def logout():
        session.pop('logged_in', None)
        print('logging you out')
        return redirect(url_for('index'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        newUsername = request.form.get("username")
        newEmail = request.form.get("email")
        newPassword = request.form.get("password")

        # Use class to register the user
        try:
            newUser = User()
            newUser.addUser(newUsername, newEmail, newPassword)
        except Exception as e:
            return render_template("register.html", error = str(e))
        else:
            session['logged_in'] = True
            return render_template("register.html", message="Account succesfully created!")
