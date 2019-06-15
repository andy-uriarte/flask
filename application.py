import os, requests

from flask import Flask, flash, session, jsonify, redirect, url_for, render_template, request, abort
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from pprint import pprint
from dbsetup import createUsers, createBooks, createReviews
from importBooks import importBooks
from models import User, Books
from helpers import *

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

@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    userID = session['user_id']
    activeUser = User(userID)
    session['books'] = []
    result = None
    if request.method == "POST":
        requestedBook = request.form.get("search")
        if not requestedBook:
            return render_template("dash.html", userName = activeUser.username, result = False)
        books = Books(requestedBook, requestedBook, requestedBook)
        for x in books.searchResults:
            session['books'].append(x)
        if not session['books']:
            result = False
        else:
            result = True
    return render_template("dash.html", userName = activeUser.username, bookResults= session['books'], result = result)

@app.route("/book/<string:book_isbn>", methods=['GET', 'POST'])
@login_required
def show_book(book_isbn):
    if book_isbn is None:
        abort(404)
    else:
        #Check if the book is in already in the session rather than hit the DB first
        for x in session['books']:
            if x.isbn == book_isbn:
                break
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "Cdjuz7jTYIwy5Jj9GhY9sw", "isbns": book_isbn})
        averageRating = res.json()['books'][0]['average_rating']
        return render_template("book.html", book=x, averageRating = averageRating)
        #Session lookup failed, someone is going for a manual hit via the URL. Check the DB
        isbnSearch = Books(book_isbn)
        if not isbnSearch.searchResults:
            abort(404)
        else:
            # Call the goodreads API
            return render_template("book.html", book=isbnSearch.searchResults)

    return render_template("book.html", book=book_isbn)

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
            return render_template("login.html", message='Incorrect credentials, please try again')
        else:
            session['logged_in'] = True
            session['user_id'] = userID[0]
            return redirect(url_for('index'))

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
