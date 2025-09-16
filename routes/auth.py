from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import create_user, get_user, check_password

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    print("Signup request received") 
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    mood = data.get("mood")

    if not name or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    user = create_user(name, email, password, mood)
    if not user:
        return jsonify({"error": "Email already registered"}), 400

    token = create_access_token(identity=email)
    return jsonify({
        "token": token,
        "name": user["name"],
        "email": user["email"],
        "mood": user.get("mood")
    })


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = get_user(email)
    if not user or not check_password(user, password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=email)
    return jsonify({
        "token": token,
        "name": user["name"],
        "email": user["email"],
        "mood": user.get("mood")
    })
