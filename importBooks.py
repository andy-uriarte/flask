import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))

db = scoped_session(sessionmaker(bind=engine))

def importBooks():
    # Check if import has run already
    runImport = db.execute("SELECT COUNT(*) from books").fetchall()
    count = runImport[0][0]
    print(count)
    if (count == 0):
        f = open('books.csv')
        reader = csv.reader(f)
        next(reader)
        for isbn, title, author, year in reader:
            print(year)
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                {"isbn": isbn, "title": title, "author": author, "year": year})
            print(f'Added {title} by {author} from {year} and a isbn of {isbn}')
        db.commit()
    else:
        print('Has already run, import skipped')

