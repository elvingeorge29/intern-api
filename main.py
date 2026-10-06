from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class BookIn(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)

books = [
    {"id": 1, "title": "Dune", "author": "Frank Herbert"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 3, "title": "The Hobbit", "author": "J.R.R. Tolkien"},
]

def find_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    return None

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
    book = find_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books", status_code=201)
def create_book(book: BookIn):
    new_id = max([b["id"] for b in books]) + 1
    
    new_book = {"id": new_id, "title": book.title, "author": book.author}
    
    books.append(new_book)
    
    return new_book

@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: BookIn):
    book = find_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book["title"] = updated_book.title
    book["author"] = updated_book.author
    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    book = find_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    books.remove(book)
    return book