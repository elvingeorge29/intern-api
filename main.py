from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import psycopg2   

app = FastAPI()

POSTGRES_LOGIN = {
    "host": "localhost",
    "database": "booksdb",
    "user": "booksuser",
    "password": "bookspass"
}

class BookIn(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/books")
def get_all_books():                 
    conn = psycopg2.connect(**POSTGRES_LOGIN)                       #Connection to Postgres/Call database
    with conn.cursor() as cur:                                      #Control database directory 
        cur.execute("SELECT * FROM books ORDER BY id")              #Gives all the books in order
        rows = cur.fetchall()                                       #Return statement (fetch data)                
    conn.close()                                                    #Close the connection 
    return rows                                                     #Return to Postman

@app.get("/books/{book_id}")
def get_book(book_id: int):
    conn = psycopg2.connect(**POSTGRES_LOGIN)                       #Connection to Postgres/Call Database
    with conn.cursor() as cur:                                      #Control Database Directory  
        cur.execute("SELECT * FROM books WHERE id = %s", (book_id,))    #Filters based on the book ID typed in the URL 
        row = cur.fetchone()                                        #Grab the desired result user asks for 
    conn.close()                                                    #Close the connection
    if row is None:                                                 #If Statement for Error Input 
        raise HTTPException(status_code=404, detail= "Book Not Found")  #Display Errror for invalid Input
    return row                                                      #Return the book


@app.post("/books", status_code=201)
def create_book(book: BookIn):
    conn = psycopg2.connect(**POSTGRES_LOGIN)                       #Connection to Postgres/Call Database
    with conn.cursor() as cur:                                      #Control Database Directory 
        cur.execute(
            "INSERT INTO books (title, author) VALUES (%s, %s) RETURNING *",     #Create a New Book
                    (book.title, book.author)                       #The values that go in the % placeholders 
                )
        new_row = cur.fetchone()                                    #Take the row just created 
    conn.commit()                                                   #Save changes to the database 
    conn.close()                                                    #Close the connection 
    return new_row                                                  #Return the new book 


@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: BookIn):
    conn = psycopg2.connect(**POSTGRES_LOGIN)                       #Connect to Postgres/Call Database
    with conn.cursor() as cur:                                      #Control Database Directory 
        cur.execute(
                "UPDATE books SET title = %s, author = %s WHERE id = %s RETURNING *",      #Update the book
            (updated_book.title, updated_book.author, book_id)      #Values that go for the Placeholders (%) 
            )
        row = cur.fetchone()                                        #Grab the Updated Row 
        conn.commit()                                               #Save Changes 
        conn.close()                                                #Close the connection 
        if row is None:                                             #If statement for any wrong book ID's are entered
            raise HTTPException(status_code=404, detail="Book Not Found")
        return row                                                  #Return the updated book
    

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    conn = psycopg2.connect(**POSTGRES_LOGIN)                       #Connect to Postgres Database 
    with conn.cursor() as cur:                                      #Control Database Directory 
        cur.execute("DELETE FROM books WHERE id = %s RETURNING *",  #Delete and return deleted row 
                    (book_id),
                    )
        row = cur.fetchone()                                        #Grab the deleted row 
        conn.commit()                                               #Save changes 
        conn.close()                                                #Close the connection 
        if row is None:                                             #If statement for if a book was not found
            raise HTTPException(status_code=404, detail="Book Not Found")
        return row                                                  #Return the deleted book