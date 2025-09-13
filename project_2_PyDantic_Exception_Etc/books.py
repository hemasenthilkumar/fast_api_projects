from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Book:

    def __init__(self, id, title, author, description, rating):
        self.id = id 
        self.title = title 
        self.author = author 
        self.description = description
        self.rating = rating 

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not created on create", default=None) 
    title: str = Field(min_length = 5)
    author: str = Field(min_length = 3)
    description: str = Field(min_length = 5, max_length=100)
    rating: int = Field(gt = -1, lt =6)

    model_config = {
        "json_schema_extra" : {
            "example": {
                "title": "A new book",
                "author": "coding",
                "description": "This is a very good book",
                "rating":5
            }
        }

    }

BOOKS = [
    Book(1, 'Computer Science Pro', 'Kayne West', 'Good book', 4),
    Book(2, 'FastAPI in Action', 'John Doe', 'Great introduction to FastAPI', 5),
    Book(3, 'Deep Learning Basics', 'Jane Smith', 'Covers the fundamentals of deep learning', 4),
    Book(4, 'Python Tricks', 'Dan Bader', 'Handy tips and tricks for Python developers', 5),
    Book(5, 'Clean Code', 'Robert C. Martin', 'Classic book on writing maintainable code', 5),
    Book(6, 'Design Patterns Explained', 'Alan Shalloway', 'Simplified explanation of design patterns', 4),
]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}")
async def read_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book 
    return "Not Found" 

@app.get("/books/")  # query parameter and with additional /
async def read_book_by_rating(book_rating: int):
    books = []
    for book in BOOKS:
        if book.rating == book_rating:
            books.append(book)
    return books

@app.post("/create-book")
async def create_book(book_request: BookRequest): # this doesnt not do any validation
    new_book = Book(**book_request.model_dump())
    BOOKS.append(attach_book_id(new_book))
 
"""
Pydantics - data modelling, data parsing and has efficient error handling
"""

def attach_book_id(book: Book):
    book.id = BOOKS[-1].id + 1 if len(BOOKS) > 0 else 1
    return book

#@app.put("/books/update_book")