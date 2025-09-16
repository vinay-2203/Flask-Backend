from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.auth import auth_bp

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key"  # Change for production
CORS(app)

jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
