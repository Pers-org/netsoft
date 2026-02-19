from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import psycopg

conn = psycopg.connect("dbname=books user=postgress_user password=postgress_password host=db")

cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL
    );
    '''
)

conn.commit()

# Init FastAPI
app = FastAPI()

# Create Book class with pydantic
class Book(BaseModel):
    id: int | None = None
    title: str
    author: str
    description: str | None = None
    price: float
    
book_db = [{
  "id": 1,
  "title": "Clean Code",
  "author": "Robert C. Martin",
  "description": "A handbook of agile software craftsmanship",
  "price": 39.99,
}]

# GET endpoint. Return all books from db
@app.get("/books")
def get_books():
    cur.execute("SELECT id, title, author, description, price FROM books;")
    rows = cur.fetchall()
    
    return_books = []

    for row in rows:
        return_books.append(
        {
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "description": row[3],
            "price": float(row[4]),
        }
        )

    return return_books

# GET endpoint. Return book with received id
@app.get("/books/{id}")
def get_book(id: int):
    cur.execute(
        "SELECT * FROM books WHERE id = %s;",
        (id,)
    )
    
    row = cur.fetchone()
    
    if row is not None:
        return {
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "description": row[3],
            "price": float(row[4]),
        }
    
    # return 404, if book not in db
    raise HTTPException(status_code=404, detail="Book not found")

# POST endpoint. Write new book to db
@app.post("/books")
def post_book(book: Book):    
    cur.execute(
    """
    INSERT INTO books (title, author, description, price)
    VALUES (%s, %s, %s, %s)
    RETURNING id;
    """,
    (book.title, book.author, book.description, book.price)
    )
    
    id = cur.fetchone()[0]
    
    cur.execute(
        "SELECT * FROM books WHERE id = %s;",
        (id,)
    )
    
    row = cur.fetchone()
    
    return {
        "id": row[0],
        "title": row[1],
        "author": row[2],
        "description": row[3],
        "price": float(row[4]),
    }
    
# PUT endpoint. Update book in db
@app.put("/books/{id}")
def update_book(id: int, new_book: Book):
    cur.execute(
        "SELECT * FROM books WHERE id = %s;",
        (id,)
    )
    
    row = cur.fetchone()
    
    if row is not None:
        cur.execute(
            """
            UPDATE books SET 
                title = %s,
                author = %s,
                description = %s,
                price = %s
            WHERE id = %s
            RETURNING id;
            """,
            (new_book.title, new_book.author, new_book.description, new_book.price, id,)
        )
        
        id = cur.fetchone()[0]
    
        cur.execute(
            "SELECT * FROM books WHERE id = %s;",
            (id,)
        )
        
        row = cur.fetchone()
        
        return {
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "description": row[3],
            "price": float(row[4]),
        }

    # return 404, if book not in db
    raise HTTPException(status_code=404, detail="Book not found")

# DELETE endpoint. Delete book from db
@app.delete("/books/{id}")
def delete_book(id: int):
    cur.execute(
        "SELECT * FROM books WHERE id = %s;",
        (id,)
    )
    
    row = cur.fetchone()
    
    if row is not None:
        cur.execute(
            "DELETE FROM books WHERE id = %s",
        (id,) 
        )
        
        return {
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "description": row[3],
            "price": float(row[4]),
        }
    
    
    raise HTTPException(status_code=404, detail="Book not found")