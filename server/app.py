import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from datetime import timedelta
from extension import db

# -------------------------------------------------
# ENV
# -------------------------------------------------
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# 👉 ruta absoluta a client/dist
CLIENT_DIST = os.path.join(BASE_DIR, "..", "client", "dist")

# -------------------------------------------------
# FLASK APP
# -------------------------------------------------
app = Flask(
    __name__,
    static_folder=os.path.join(CLIENT_DIST, "assets"),
    template_folder=CLIENT_DIST
)

CORS(app, supports_credentials=True)

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
    days=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 7))
)

# FIX: Neon Postgres + SQLAlchemy
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 280,
    "pool_size": 5,
    "max_overflow": 10,
}

print("Loaded DB:", app.config["SQLALCHEMY_DATABASE_URI"])
print("Serving React from:", CLIENT_DIST)

# -------------------------------------------------
# EXTENSIONS
# -------------------------------------------------
db.init_app(app)
jwt = JWTManager(app)

# -------------------------------------------------
# BLUEPRINTS (API)
# -------------------------------------------------
from routes.auth import auth_bp
from routes.mistral import prompt_bp
from routes.groq import groq_bp

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(prompt_bp, url_prefix="/api/mistral")
app.register_blueprint(groq_bp, url_prefix="/api/groq")

# -------------------------------------------------
# DATABASE
# -------------------------------------------------
with app.app_context():
    db.create_all()

# -------------------------------------------------
# SERVE REACT (VITE BUILD)
# -------------------------------------------------
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    # si el archivo existe (js, css, img, etc)
    if path != "" and os.path.exists(os.path.join(CLIENT_DIST, path)):
        return send_from_directory(CLIENT_DIST, path)

    # React Router fallback
    return send_from_directory(CLIENT_DIST, "index.html")

# -------------------------------------------------
# MAIN
# -------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
