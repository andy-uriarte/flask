import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import text

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#Define the user class for user management

class User:
    def __init__(self, user_id=None):

        # Declare main instance variables for User
        self.username = None
        self.__password = None
        self.email = None
        self.user_id = user_id
        self.isNewUser = None

        # Check if this is a new user being created or retrieved
        if self.user_id is None:
            self.isNewUser = True
        else:
            try:
                self.user_id = int(user_id)
            except ValueError:
                print('User id is not a digit')
                raise
            else:
                self.isNewUser = False
                #retrieve information about user_id
                self._populateUser()

    def _populateUser(self):
        user = db.execute("SELECT username, email, password FROM users WHERE id = :id", {"id": self.user_id}).fetchone()
        if user is None:
            raise LookupError('User id was not found')
        else:
            self.username = user.username
            self.__password = user.password
            self.email = user.email
            return True


    def addUser(self, username, email, password):
        self.username = username
        self.__password = password
        self.email = email

        # Check if username is available and insert the user if so
        try:
            newUser = db.execute("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)", {"username": self.username, "email": self.email, "password": self.__password})
        except:
            raise LookupError("Username is taken")
        else:
            db.commit()
            return True

    def removeUser(self):
        if self.isNewUser == True:
            print('Not going to delete')
            return False
        try:
            deleteUser = db.execute("DELETE FROM users WHERE id = :id", {"id": self.user_id})
        except:
            raise LookupError("User not found, unable to delete")
        else:
            print('I ran the delete')
            db.commit()
            return True

