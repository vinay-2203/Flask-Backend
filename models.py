import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

DATA_FILE = "users.json"

def load_users():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

def create_user(name, email, password, mood=None):
    users = load_users()
    if any(u["email"] == email for u in users):
        return None
    user = {
        "name": name,
        "email": email,
        "password": generate_password_hash(password),
        "mood": mood
    }
    users.append(user)
    save_users(users)
    return user

def get_user(email):
    users = load_users()
    return next((u for u in users if u["email"] == email), None)

def check_password(user, password):
    return check_password_hash(user["password"], password)
