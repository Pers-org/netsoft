import pytest
from fastapi.testclient import TestClient
from app.API import app, book_db

client = TestClient(app)

# clear db before any test
@pytest.fixture(autouse=True)
def clear_db():
    book_db.clear()
    yield


# TEST GET (for all books)
def test_get_all_books_empty():
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == []

# TEST PUT
def test_create_book():
    data = {
        "title": "War and Peace",
        "author": "Leo Tolstoy",
        "description": "Very boring book",
        "price": 666.666
    }

    # send data
    response = client.post("/books", json=data)

    # check return code
    assert response.status_code == 200
    body = response.json()

    # check fields
    assert body["title"] == data["title"]
    assert body["author"] == data["author"]
    assert body["price"] == data["price"]
    assert "id" in body


# Test GET by id
def test_get_book_by_id():
    # POST book
    response = client.post("/books", json={
        "title": "bla",
        "author": "bla-bla",
        "description": "bla-bla-bla",
        "price": 10
    })
    book = response.json()

    # check book existing (by id)
    response = client.get(f"/books/{book['id']}")
    
    assert response.status_code == 200
    assert response.json()["id"] == book["id"]


# Test PUT
def test_update_book():
    response = client.post("/books", json={
        "title": "Old",
        "author": "Author",
        "price": 10
    })
    book = response.json()

    updated_data = {
        "title": "New",
        "author": "Author",
        "price": 20
    }

    response = client.put(f"/books/{book['id']}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["title"] == "New"
    assert response.json()["price"] == 20


# Test DELETE

def test_delete_book():
    # post book
    response = client.post("/books", json={
        "title": "Delete",
        "author": "Author",
        "price": 15
    })
    book = response.json()

    # delete this book
    response = client.delete(f"/books/{book['id']}")
    assert response.status_code == 200

    # check book with help GET
    response = client.get(f"/books/{book['id']}")
    assert response.status_code == 404
