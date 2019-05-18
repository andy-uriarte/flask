import os

from flask import Flask, session, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from pprint import pprint
from dbsetup import createUsers, createBooks, createReviews
from importBooks import importBooks


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

    if session['logged_in']:
            return '<h1>You are logged in!</h1>'
    else:
        session.pop('logged_in', None)
        return f'<h2>Access Denied</h2>'

@app.route("/register")
def register():
    return '<h1>This is the registration page</h1>'
