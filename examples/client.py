import requests
import json 

# Демонстрация взаимодействия с API по HTTP

URL = "https://jsonplaceholder.typicode.com"

# GET запрос на получение всех записей
all_notes = requests.get(URL+"/posts")
all_notes = all_notes.json()

print("All notes:", all_notes)

# GET запрос на получение одной записи

note = requests.get(URL+"/posts/10")
note = note.json()

print("Single note:", note)

# POST запрос на создание записи

user = {
    "userId": 1362,
    "id": 1363,
    "title": "Bla-bla-bla",
    "body": "Bla-bla-bla"
}

response = requests.post(URL+"/posts", json=user)

print("Response status:", response)
