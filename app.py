from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from routes.auth import auth_bp
from routes.profile import profile_bp

app = Flask(__name__)

# 🔑 Config
app.config["JWT_SECRET_KEY"] = "super-secret-key"  # change this in production
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600  # 1 hour

CORS(app)
jwt = JWTManager(app)

# 🔹 Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(profile_bp, url_prefix="/api")

@app.route("/api")
def home():
    return {"msg": "Backend is running!"}, 200

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))  # for Render/Heroku deploy
    app.run(host="0.0.0.0", port=port, debug=True)
