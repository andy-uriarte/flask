from functools import wraps
from flask import request, redirect, url_for, session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("logged_in") is None:
            return redirect(url_for('login', message='Please login'))
        return f(*args, **kwargs)
    return decorated_function
