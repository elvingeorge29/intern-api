from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class BookIn(BaseModel):
    title: str
    author: str

books = [
    {"id": 1, "title": "Dune", "author": "Frank Herbert"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 3, "title": "The Hobbit", "author": "J.R.R. Tolkien"},
]

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/books")
def get_all_books(author: Optional[str] = None):
    if author is None:
        return books
    
    filtered_books = [book for book in books if book["author"] == author]
    return filtered_books

@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
            
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books", status_code=201)
def create_book(book: BookIn):
    # 1. Figure out the next ID
    new_id = max([b["id"] for b in books]) + 1
    
    # 2. Create the new book dictionary
    new_book = {"id": new_id, "title": book.title, "author": book.author}
    
    # 3. Add it to our "database"
    books.append(new_book)
    
    # 4. Return the new book
    return new_book