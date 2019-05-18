import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import text

# Check for environment variable
if not os.getenv("DATABASE_URL"):
     raise RuntimeError("DATABASE_URL is not set")
else:
   print("Database detected in dbsetup, running application")
# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Create the database tables
def createUsers():
    print('initializing the users table')
    try:
        db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(50) NOT NULL)""")
        db.commit()
    except:
        print("The users table initialization failed")
        return False
    else:
        print("The users table initialized succesfully")
        return True

def createBooks():
    print('initializing the books table')
    try:
        db.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id SERIAL PRIMARY KEY,
            isbn VARCHAR(50) UNIQUE NOT NULL,
            title VARCHAR(50) NOT NULL,
            author VARCHAR(50) NOT NULL,
            year INTEGER NOT NULL)""")
        db.commit()
    except:
        print("The books table failed to create")
        return False
    else:
        print("The books table was succesfully created")
        return True

def createReviews():
    print('initializing the reviews table')
    try:
        db.execute("""
        CREATE TABLE IF NOT EXISTS reviews(
            id SERIAL PRIMARY KEY,
            rating INTEGER NOT NULL,
            review VARCHAR NOT NULL,
            user_id INTEGER REFERENCES users(id),
            book_id INTEGER REFERENCES books(id))""")
        db.commit()
    except:
        print("The reviews table failed to create")
        return False
    else:
        print("The books table was succesfully created")
        return True
