from flask import Flask
import signal
import sys
import uuid
import json
from fastapi import Body, status
from fastapi.responses import JSONResponse

app = Flask(__name__)

class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.id = str(uuid.uuid4())
        
user_db = []


@app.route("/")
def test():
    return """ 
        <div style="text-align:center; padding-top:250px;">
            <img src="https://media.tenor.com/IB9ol7welioAAAAM/dance-vibing.gif">
        </div>
        """

@app.get("/")
async def get():
    return JSONResponse(json.dumps(user_db))

@app.post("/")
def add_user(data  = Body()):
    user = User(data["name"], data["age"])
    user.append(user)
    return user

@app.put("/")
def edit_user(data  = Body()):
    target_id = data["id"]
    
    for user in user_db:
        if user.id == target_id:
            user.name = data["name"]
            user.age = data["age"]
            return user
        
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={ "message": "User not found" })

@app.delete("/")
def delete_user(data  = Body()):
    target_id = data["id"]
    
    for user in user_db:
        if user.id == target_id:
            user_db.remove(user)
            return user
        
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={ "message": "User not found" })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
