from fastapi import FastAPI 

app = FastAPI()

BOOKS = [
    {
        "title": "System Design Fundamentals",
        "author": "Martin Fowler",
        "category": "Software Architecture"
    },
    {
        "title": "Deep Dive into Python",
        "author": "Luciano Ramalho",
        "category": "Programming"
    },
    {
        "title": "Machine Learning for Humans",
        "author": "Vishal Maini",
        "category": "Artificial Intelligence"
    },
    {
        "title": "Design Patterns Explained",
        "author": "Alan Shalloway",
        "category": "Software Engineering"
    }
]



# this has to come first as this will called.
# the more generic it is, more we have to move up
@app.get("/books")
async def read_all_books():   # async is not required in FastAPI
    return BOOKS


# path parameters

@app.get("/books/{title}")
def read_book(title: str):
    for book in BOOKS:
        if book['title'].casefold() == title.casefold():
            return {'book': book}
    return {'msg': '404 Not Found'}

# query parameters
# can be used with path paramters
@app.get("/books")
def read_book_by_category_query(category: str):
    result = []
    print("Hi")
    for book in BOOKS:
        if book['category'].lower() == category.lower():
            result.append(book)
    return result

@app.get("/books/byauthor")
def read_book_by_author_query(author: str):
    result = []
    for book in BOOKS:
        if book['author'].lower() == author.lower():
            result.append(book)
    return result

@app.get("/books/{book_author}")
def read_author_category_query(book_author: str, category: str):
    result = []
    for book in BOOKS:
        if book['author'].lower()==book_author.lower() and \
            book['category'].lower() == category.lower():
            result.append(book)
    return result    



# uvicorn books:app --reload