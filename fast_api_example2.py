

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

# Initialize FastAPI app
app = FastAPI(
    title="Book Management API",
    description="A simple API to manage books with automatic Swagger documentation",
    version="1.0.0"
)

# Pydantic models for request/response validation
class Genre(str, Enum):
    FICTION = "fiction"
    NON_FICTION = "non-fiction"
    SCIENCE = "science"
    TECHNOLOGY = "technology"

class BookBase(BaseModel):
    title: str
    author: str
    genre: Genre
    price: float
    
class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    
    class Config:
        from_attributes = True

# Simulate a database with a list
books_db = []
book_id_counter = 1

@app.post("/books/", response_model=Book, tags=["books"])
async def create_book(book: BookCreate):
    """
    Create a new book with the following parameters:
    
    - **title**: Book title
    - **author**: Book author
    - **genre**: Book genre (must be one of: fiction, non-fiction, science, technology)
    - **price**: Book price
    """
    global book_id_counter
    new_book = Book(
        id=book_id_counter,
        **book.model_dump()
    )
    books_db.append(new_book)
    book_id_counter += 1
    return new_book

@app.get("/books/", response_model=List[Book], tags=["books"])
async def list_books(
    genre: Optional[Genre] = Query(None, description="Filter books by genre"),
    min_price: Optional[float] = Query(None, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, description="Maximum price filter")
):
    """
    Get all books with optional filtering by:
    
    - **genre**: Book genre
    - **min_price**: Minimum price
    - **max_price**: Maximum price
    """
    filtered_books = books_db

    if genre:
        filtered_books = [book for book in filtered_books if book.genre == genre]
    if min_price is not None:
        filtered_books = [book for book in filtered_books if book.price >= min_price]
    if max_price is not None:
        filtered_books = [book for book in filtered_books if book.price <= max_price]

    return filtered_books

@app.get("/books/{book_id}", response_model=Book, tags=["books"])
async def get_book(
    book_id: int = Path(..., description="The ID of the book to retrieve", gt=0)
):
    """
    Get a specific book by its ID
    """
    book = next((book for book in books_db if book.id == book_id), None)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=Book, tags=["books"])
async def update_book(
    book_id: int = Path(..., description="The ID of the book to update", gt=0),
    book_update: BookCreate = None
):
    """
    Update a book by its ID
    """
    book_idx = next((idx for idx, book in enumerate(books_db) if book.id == book_id), None)
    if book_idx is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    updated_book = Book(id=book_id, **book_update.model_dump())
    books_db[book_idx] = updated_book
    return updated_book

@app.delete("/books/{book_id}", tags=["books"])
async def delete_book(
    book_id: int = Path(..., description="The ID of the book to delete", gt=0)
):
    """
    Delete a book by its ID
    """
    book_idx = next((idx for idx, book in enumerate(books_db) if book.id == book_id), None)
    if book_idx is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    books_db.pop(book_idx)
    return {"message": f"Book with ID {book_id} has been deleted"}

# Add example data
@app.on_event("startup")
async def add_sample_data():
    sample_books = [
        {
            "title": "The Python Way",
            "author": "John Smith",
            "genre": Genre.TECHNOLOGY,
            "price": 29.99
        },
        {
            "title": "Digital Future",
            "author": "Sarah Johnson",
            "genre": Genre.SCIENCE,
            "price": 24.99
        }
    ]
    
    for book in sample_books:
        await create_book(BookCreate(**book))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

