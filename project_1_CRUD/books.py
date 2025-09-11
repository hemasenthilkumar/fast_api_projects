from fastapi import Body, FastAPI 

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

@app.get("/books/{book_title}")
def read_book(book_title: str):
    for book in BOOKS:
        if book['title'].casefold() == book_title.casefold():
            return {'book': book}
    return {'msg': '404 Not Found'}

# query parameters
# can be used with path paramters
@app.get("/books/")
def read_book_by_category_query(category: str):
    result = []
    print("Hi")
    for book in BOOKS:
        if book['category'].lower() == category.lower():
            result.append(book)
    return result

@app.get("/books/byauthor/")
def read_book_by_author_query(author: str):
    result = []
    for book in BOOKS:
        if book['author'].lower() == author.lower():
            result.append(book)
    return result

@app.get("/books/{book_author}/")
def read_author_category_query(book_author: str, category: str):
    result = []
    for book in BOOKS:
        if book['author'].lower()==book_author.lower() and \
            book['category'].lower() == category.lower():
            result.append(book)
    return result    


@app.post('/books/create_book')
def create_book(new_book=Body()):
    BOOKS.append(new_book)

@app.put('/books/update_book')
def update_book(new_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i]['title'].lower() == new_book['title'].lower():
            BOOKS[i] = new_book

@app.delete('/books/delete_book/{book_title}')
def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i]['title'].lower() == book_title.lower():
            BOOKS.pop(i)
            break


# uvicorn books:app --reload