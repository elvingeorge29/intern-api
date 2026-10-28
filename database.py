from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from config import DATABASE_URL 

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)   #How data is requested  
Base = declarative_base()                                                           #Base Class for our models

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close() 