from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

# Temporary in-memory storage for users
users = {}

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        
        if not name or not email or not password:
            return render_template("register.html", error="All fields are required")

        if email in users:
            return render_template("register.html", error="Email already exists")
        
        if len(password) < 6:
            return render_template("register.html", error="Password must be at least 6 characters")

        users[email] = {
            'id': len(users) + 1,
            'name': name,
            'email': email,
            'password_hash': generate_password_hash(password)
        }

        return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        if not email or not password:
            return render_template("login.html", error="Email and password are required")

        user = users.get(email)
        if user and check_password_hash(user['password_hash'], password):
            session["user_id"] = user['id']
            session["user_name"] = user['name']
            return redirect("/dashboard")
        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

