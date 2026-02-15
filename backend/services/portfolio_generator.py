from backend.services.grok_service import generate_portfolio_with_grok

def generate_portfolio(user, data):
    """Generate portfolio using user data and AI enhancement"""
    if not user:
        raise ValueError("User data is required to generate portfolio")

    # Check if AI enhancement is requested (default to True)
    use_ai = data.get('use_ai', True) if data else True

    if use_ai:
        return generate_ai_enhanced_portfolio(user, data)
    else:
        return generate_basic_portfolio(user, data)

def generate_basic_portfolio(user, data):
    """Generate basic portfolio from user data"""
    portfolio = f"{user.name}'s Portfolio\n"
    portfolio += "=" * (len(user.name) + 12) + "\n\n"

    if user.profile:
        if user.profile.headline:
            portfolio += f"Headline: {user.profile.headline}\n\n"
        if user.profile.summary:
            portfolio += f"About Me:\n{user.profile.summary}\n\n"
        if user.profile.projects:
            portfolio += f"Projects:\n{user.profile.projects}\n\n"
        if user.profile.skills:
            portfolio += f"Skills:\n{user.profile.skills}\n\n"
    else:
        portfolio += "Note: Please complete your profile to showcase your projects and skills in a comprehensive portfolio.\n"

    portfolio += f"Contact: {user.email}\n"
    return portfolio

def generate_ai_enhanced_portfolio(user, data):
    """Generate AI-enhanced portfolio"""
    # Prepare user profile data
    profile = user.profile if user.profile else None
    
    skills = profile.skills.split(',') if profile and profile.skills else []
    skills = [s.strip() for s in skills if s.strip()]
    
    projects = profile.projects.split('|') if profile and profile.projects else []
    projects = [p.strip() for p in projects if p.strip()]
    
    experience = profile.experience.split('|') if profile and profile.experience else []
    experience = [e.strip() for e in experience if e.strip()]
    
    education = profile.education.split('|') if profile and profile.education else []
    education = [e.strip() for e in education if e.strip()]
    
    profile_data = {
        "name": user.name,
        "email": user.email,
        "headline": profile.headline if profile and profile.headline else "",
        "summary": profile.summary if profile and profile.summary else "",
        "skills": skills,
        "projects": projects,
        "experience": experience,
        "education": education
    }

    try:
        # Use Grok API for professional portfolio generation
        portfolio = generate_portfolio_with_grok(profile_data)
        return portfolio

    except Exception as e:
        print(f"AI portfolio generation failed: {e}")
        return generate_basic_portfolio(user, data)
