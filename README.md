# Book API

A simple REST API built with FastAPI to manage a collection of books. It supports all four CRUD operations, automatic data validation, and error handling.

## Setup

1. Create a virtual environment: `python -m venv venv`
2. Activate it:
   - Mac/Linux: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`

## Run

Start the server with:
```bash
uvicorn main:app --reload

Once running, you can access the API at http://127.0.0.1:8000 and the interactive docs at http://127.0.0.1:8000/docs.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/books` | List all books (optional `?author=` filter) |
| GET | `/books/{book_id}` | Get one book by its id |
| POST | `/books` | Create a new book |
| PUT | `/books/{book_id}` | Update an existing book |
| DELETE | `/books/{book_id}` | Delete a book |

## Testing
Make sure your virtual environment is active, then run:
```bash
python -m pytest -v

**4. Commit and Push**
Stop the server if it's running (`Ctrl + C`), then run:
```bash
git add .
git commit -m "Complete test suite with API key protection and bug-catching proof"
git push

## Project Structure
- `main.py`: The entry point. Connects the routers and initializes the app.
- `schemas.py`: Pydantic models for data validation.
- `routers/books.py`: All the endpoints for the `/books` resource.
- `models.py`: SQLAlchemy database models.