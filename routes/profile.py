from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import get_user, save_users, load_users

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/api/profile", methods=["GET"])
@jwt_required()
def profile():
    email = get_jwt_identity()
    user = get_user(email)
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user)


@profile_bp.route("/api/mood", methods=["POST"])
@jwt_required()
def update_mood():
    data = request.get_json()
    new_mood = data.get("mood")
    if not new_mood:
        return jsonify({"error": "Mood is required"}), 400

    email = get_jwt_identity()
    users = load_users()
    user = next((u for u in users if u["email"] == email), None)

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Update mood
    user["mood"] = new_mood
    save_users(users)

    return jsonify({"msg": "Mood updated", "mood": new_mood})
