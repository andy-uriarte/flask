import os

from flask import Flask, session, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from pprint import pprint
from logic import adder

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


@app.route("/")
def index():
    
    first_num = int(input("Please provide a number:"))
    value = adder(first_num, 2)
    
    if 'logged_in' not in session:
        session['logged_in'] = False

    if session['logged_in']:
            return '<h1>You are logged in!</h1>'
    else:
        session.pop('logged_in', None)
        print(session.get('logged_in'))
        return f'<h1>Access Denied!, {value}</h1>', 403
