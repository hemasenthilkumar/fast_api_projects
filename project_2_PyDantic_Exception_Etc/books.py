from typing import Optional
from fastapi import FastAPI, Path, Query # this is for validating path, query parameters
from fastapi import HTTPException
from pydantic import BaseModel, Field
from starlette import status # explictly put the status

"""
Pydantics - data modelling, data parsing and has efficient error handling

Status codes - help the client (user/system) with happened on the server, they are internation standard
they denote whether the request was successful or not

1xx = Information Response Eg: Request progressing
2xx = Success Eg: Request completed sucessfully
3xx = Redirection. Eg: Further action required
4xx = Client side error Eg: Wrong input, authentication issues
5xx = Server side error Eg: Internal server error

200 = OK, standard response, commonly used for GET
201 = Successful, created a new resource, used a lot in POST
204 = Successful but didnt return anything nor created an entity , commonly used in PUT

400 = Bad Request = Invalid request methods
401 = Unauthorized
404 = Not Found
422 = Unprocessable (semantic errors)

501 = Generic error message , when unexpected issue happened in the server
"""

app = FastAPI()

class Book:

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id 
        self.title = title 
        self.author = author 
        self.description = description
        self.rating = rating 
        self.published_date = published_date

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not created on create", default=None) 
    title: str = Field(min_length = 5)
    author: str = Field(min_length = 3)
    description: str = Field(min_length = 5, max_length=100)
    rating: int = Field(gt = 0, lt =6)
    published_date: int = Field(gt=1996, lt=2025)

    model_config = {
        "json_schema_extra" : {
            "example": {
                "title": "A new book",
                "author": "coding",
                "description": "This is a very good book",
                "rating":5,
                "published_date": 1996
            }
        }

    }

BOOKS = [
    Book(1, 'Computer Science Pro', 'Kayne West', 'Good book', 4, 2001),
    Book(2, 'FastAPI in Action', 'John Doe', 'Great introduction to FastAPI', 5, 2002),
    Book(3, 'Deep Learning Basics', 'Jane Smith', 'Covers the fundamentals of deep learning', 4, 2002),
    Book(4, 'Python Tricks', 'Dan Bader', 'Handy tips and tricks for Python developers', 5, 2002),
    Book(5, 'Clean Code', 'Robert C. Martin', 'Classic book on writing maintainable code', 5, 2001),
    Book(6, 'Design Patterns Explained', 'Alan Shalloway', 'Simplified explanation of design patterns', 4, 1996),
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book  
    raise HTTPException(status_code=404, detail='Item not found!')

@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_book_by_date(published_date: int = Query(gt=1996, lt=2025)):
    books = []
    for book in BOOKS:
        if book.published_date == published_date:
            books.append(book)
    return books    

@app.get("/books/", status_code=status.HTTP_200_OK)  # query parameter and with additional /
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books = []
    for book in BOOKS:
        if book.rating == book_rating:
            books.append(book)
    return books

@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest): # this doesnt not do any validation
    new_book = Book(**book_request.model_dump())
    BOOKS.append(attach_book_id(new_book))
 
def attach_book_id(book: Book):
    book.id = BOOKS[-1].id + 1 if len(BOOKS) > 0 else 1
    return book

@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    # this will fail if id is None
    is_updated = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book 
            is_updated = True
    if not is_updated:
        raise HTTPException(status_code=404, detail='Item not found to update!')

@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    is_deleted = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            is_deleted = True
            break
    if not is_deleted:
        raise HTTPException(status_code=404, detail='Item not found to delete!') 


