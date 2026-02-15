"""
Profile routes for user profile management
"""
from flask import Blueprint, render_template, request, redirect, url_for, session

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/dashboard')
def dashboard():
    """User dashboard"""
    if 'user_id' not in session:
        return redirect('/login')
    if 'user_name' not in session:
        return redirect('/login')
    return render_template('dashboard.html', user_name=session.get('user_name'))

@profile_bp.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        headline = request.form.get("headline")
        phone = request.form.get("phone")
        linkedin = request.form.get("linkedin")
        github = request.form.get("github")
        email = request.form.get("email")
        leetcode = request.form.get("leetcode")
        other_links = request.form.get("other_links")
        summary = request.form.get("summary")
        skills = request.form.get("skills")
        projects = request.form.get("projects")
        experience = request.form.get("experience")
        education = request.form.get("education")
        dob = request.form.get("dob")
        languages = request.form.get("languages")
        hobbies = request.form.get("hobbies")

        # Store profile in session temporarily
        session['profile'] = {
            'headline': headline,
            'phone': phone,
            'linkedin': linkedin,
            'github': github,
            'email': email,
            'leetcode': leetcode,
            'other_links': other_links,
            'summary': summary,
            'skills': skills,
            'projects': projects,
            'experience': experience,
            'education': education,
            'dob': dob,
            'languages': languages,
            'hobbies': hobbies
        }
        return redirect("/dashboard")

    return render_template("profile.html", profile=session.get('profile', {}))
