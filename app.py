"""
Main Flask application for AI Resume Portfolio Builder
"""
import os
from flask import Flask, redirect, url_for, send_from_directory
from flask_cors import CORS
from backend.config import Config

# Determine static folder path - use build if available, otherwise use public
static_folder_path = os.path.join(os.path.dirname(__file__), 'frontend', 'build')
if not os.path.exists(static_folder_path):
    static_folder_path = os.path.join(os.path.dirname(__file__), 'frontend', 'public')

app = Flask(
    __name__,
    static_folder=static_folder_path,
    static_url_path="/",
    instance_path=os.path.join(os.path.dirname(__file__), 'backend', 'instance')
)

# Ensure instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

app.config.from_object(Config)

CORS(app)

# Register blueprints
from backend.routes.auth_routes import auth_bp
from backend.routes.profile_routes import profile_bp
from backend.routes.ai_routes import ai_bp

app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(ai_bp)

@app.route("/")
def serve():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def static_proxy(path):
    file_path = os.path.join(app.static_folder, path)
    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
