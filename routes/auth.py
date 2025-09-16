from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import load_users, save_users

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    mood = data.get("mood")

    if not name or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    users = load_users()
    if any(user["email"] == email for user in users):
        return jsonify({"error": "Email already registered"}), 400

    user = {"name": name, "email": email, "password": password, "mood": mood}
    users.append(user)
    save_users(users)

    token = create_access_token(identity=email)
    return jsonify({"token": token, "name": name, "email": email})

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    users = load_users()
    user = next((u for u in users if u["email"] == email and u["password"] == password), None)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=email)
    return jsonify({"token": token, "name": user["name"], "email": user["email"], "mood": user.get("mood")})
