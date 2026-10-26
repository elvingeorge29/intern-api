from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import psycopg2   
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()

POSTGRES_LOGIN = {
    "host": "localhost",
    "database": "booksdb",
    "user": "booksuser",
    "password": "bookspass"
}

DATABASE_URL = "postgresql+psycopg2://booksuser:bookspass@localhost:5432/booksdb"   #Connection to Postgres via creating an engine
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)   #How data is requested 

Base = declarative_base()                                                           #Base Class for our models

class Book(Base):                                               #Creates Python Class = Book
    __tablename__ = "books"                                     #Which Table in Postgres the class maps to

    id = Column(Integer, primary_key = True, index = True)      #Defines the first column id 
    title = Column(String, nullable = False)                    #Defines the title column; no null fields 
    author = Column (String, nullable = False)                  #Defines the author columnn: 

class BookIn(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/books")                              
def get_all_books():                 
    db = SessionLocal()                                             #Connecting to the Session
    books = db.query(Book).all()                                    #Requests all rows form book table
    db.close()                                                      #Closes the connection to database       
    return books                                                    #Returns the list of books 

@app.get("/books/{book_id}")
def get_book(book_id: int):
    db = SessionLocal()                                             #Coneccting to the session 
    book = db.query(Book).filter(Book.id == book_id).first()        #Asks database for first book that matches the book ID
    db.close()                                                      #Closes the connection to the databse
    if book is None:                                                #Raise Error if user inputs incorrect id/data
            raise HTTPException(status_code = 404, detail = "Book not found")   
    return book                                                     #return the specific book requested 

@app.post("/books", status_code=201)
def create_book(book: BookIn):
    db = SessionLocal()                                             #Connecting to Session
    new_book = Book(title=book.title, author=book.author)           #Creating a new Book Object 
    db.add(new_book)                                                #Add the new book to the database 
    db.commit()                                                     #Save the changes to the database 
    db.refresh(new_book)                                            #Refresh the object since we are creating a new object, not an exsisting one 
    db.close()                                                      #Close the database connection 
    return new_book                                                 #Return the new book 


@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: BookIn):
    db = SessionLocal()                                             #Connecting to Session
    book = db.query(Book).filter(Book.id == Book.id).first()        #First, find the book we want to update 
    if book is None:                                                #Make sure the book exists, if it doesn't, give 404 error and close database  
        db.close()
        raise HTTPException(status_code = 404, detail = "Book Not Found")
    book.title = updated_book.title                                 #Update the Book Title 
    book.author = updated_book.author                               #Update the Book Author 
    db.commit()                                                     #Save the changes 
    db.refresh(book)                                                #Refresh to get the latest data 
    db.close()                                                      #Close the database connection
    return book                                                     #Return the updated book 

    

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    db = SessionLocal()                                             #Connect to databse 
    book = db.query(Book).filter(Book.id == Book.id).first()        #Find the book we want to delete 
    if book is None:                                                #If the book is not found, raise a 404 error 
        db.close()
        raise HTTPException(status_code = 404, detail = "Book Not Found")
    db.delete(book)                                                 #Delete the book from the database 
    db.commit()                                                     #Save the changes 
    db.close                                                        #Close the database connection 
    return book                                                     #Return the deleted book