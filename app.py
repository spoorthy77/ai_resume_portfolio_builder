"""
Main Flask application for AI Resume Portfolio Builder
"""
import os
from flask import Flask, redirect, url_for
from flask_cors import CORS
from backend.config import Config

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static",
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

@app.route('/')
def home():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
