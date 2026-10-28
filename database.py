from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql+psycopg2://booksuser:bookspass@localhost:5432/booksdb"   #Connection to Postgres via creating an engine
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)   #How data is requested 

Base = declarative_base()                                                           #Base Class for our models

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close() 