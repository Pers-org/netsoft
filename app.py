from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.id = str(uuid.uuid4())
        
user_db = [User("Ivan", "20"), User("Andrew", "30"), User("Peter", "25")]


@app.get("/main")
def main_page():
    return """
    <div style="text-align:center; padding-top:250px;">
      <img src="https://media.tenor.com/IB9ol7welioAAAAM/dance-vibing.gif">
    </div>
    """

@app.route("/api/users", methods=["GET"])
def get_users():
    return jsonify(user_db)

@app.post("/api/users", methods=["POST"])
def add_user():
    data = request.get_json()
    user = {"id": str(uuid.uuid4()), "name": data["name"], "age": data["age"]}
    user_db.append(user)
    return jsonify(user), 201

@app.put("/api/users", methods=["PUT"])
def edit_user():
    data = request.get_json()
    target_id = data["id"]
    for user in user_db:
        if user["id"] == target_id:
            user["name"] = data["name"]
            user["age"] = data["age"]
            return jsonify(user)
    return jsonify({"message": "User not found"}), 404

@app.delete("/api/users", methods=["DELETE"])
def delete_user():
    data = request.get_json()
    target_id = data["id"]
    for i, user in enumerate(user_db):
        if user["id"] == target_id:
            deleted = user_db.pop(i)
            return jsonify(deleted)
    return jsonify({"message": "User not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
