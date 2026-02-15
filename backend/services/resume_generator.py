from backend.services.resume_templates import ResumeTemplates
from backend.services.grok_service import generate_resume_with_grok

def generate_resume(user, data):
    """Generate resume using user data and selected template

    Args:
        user: User object with profile
        data: Dictionary containing:
            - template: Template name (default: 'professional')
            - use_ai: Use AI generation (default: True)

    Returns:
        Formatted resume string
    """
    if not user:
        raise ValueError("User data is required to generate resume")

    # Check if AI enhancement is requested (default to True)
    use_ai = data.get('use_ai', True) if data else True

    if use_ai:
        # Use AI to generate optimized resume
        resume = generate_ai_enhanced_resume(user, data)
    else:
        # Generate resume using template
        template_name = data.get('template', 'professional') if data else 'professional'
        
        # Validate template name
        valid_templates = ResumeTemplates.get_all_templates()
        if template_name not in valid_templates:
            template_name = 'professional'
        
        resume = ResumeTemplates.generate_from_template(template_name, user, user.profile)

    return resume

def generate_ai_enhanced_resume(user, data):
    """Generate AI-enhanced resume content using Grok API"""
    # Prepare user profile data for Grok
    profile = user.profile if user.profile else None
    
    # Extract and format data from profile
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
        # Use Grok API for professional resume generation
        resume = generate_resume_with_grok(profile_data)
        return resume

    except Exception as e:
        print(f"AI resume generation failed: {e}")
        # Fallback to template
        return ResumeTemplates.generate_from_template('professional', user, user.profile)
