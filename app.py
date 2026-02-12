from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)
        
user_db = [
    {"id": str(uuid.uuid4()), "name": "Ivan", "age": 20},
    {"id": str(uuid.uuid4()), "name": "Andrew", "age": 30},
    {"id": str(uuid.uuid4()), "name": "Peter", "age": 25},
]

@app.route("/main", methods=["GET"])
def main_page():
    return """
    <div style="text-align:center; padding-top:250px;">
      <img src="https://media.tenor.com/IB9ol7welioAAAAM/dance-vibing.gif">
      <img src="https://media.tenor.com/IB9ol7welioAAAAM/dance-vibing.gif">
      <img src="https://media.tenor.com/IB9ol7welioAAAAM/dance-vibing.gif">
    </div>
    """

@app.get("/api/users")
def get_users():
    return jsonify(user_db)

@app.post("/api/users")
def add_user():
    data = request.get_json()
    user = {"id": str(uuid.uuid4()), "name": data["name"], "age": data["age"]}
    user_db.append(user)
    return jsonify(user), 201

@app.put("/api/users")
def edit_user():
    data = request.get_json()
    target_id = data["id"]
    for user in user_db:
        if user["id"] == target_id:
            user["name"] = data["name"]
            user["age"] = data["age"]
            return jsonify(user)
    return jsonify({"message": "User not found"}), 404

@app.delete("/api/users")
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
