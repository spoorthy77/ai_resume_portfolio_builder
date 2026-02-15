from backend.services.grok_service import generate_cover_letter_with_grok

def generate_cover_letter(user, data):
    """Generate cover letter using user data and AI enhancement"""
    if not user:
        raise ValueError("User data is required to generate cover letter")

    job_title = data.get('job_title', 'Your Target Position') if data else 'Your Target Position'
    company_name = data.get('company_name', 'the Company') if data else 'the Company'
    job_description = data.get('job_description', '') if data else ''

    # Prepare user profile data
    profile = user.profile if user.profile else None
    
    skills = profile.skills.split(',') if profile and profile.skills else []
    skills = [s.strip() for s in skills if s.strip()]
    
    experience = profile.experience.split('|') if profile and profile.experience else []
    experience = [e.strip() for e in experience if e.strip()]
    
    profile_data = {
        "name": user.name,
        "email": user.email,
        "headline": profile.headline if profile and profile.headline else "",
        "summary": profile.summary if profile and profile.summary else "A dedicated professional.",
        "skills": skills,
        "experience": experience
    }
    
    job_data = {
        "position": job_title,
        "company": company_name,
        "description": job_description
    }

    try:
        # Use Grok API for professional cover letter generation
        cover_letter = generate_cover_letter_with_grok(profile_data, job_data)
        return cover_letter

    except Exception as e:
        # Fallback to basic template if AI fails
        print(f"AI cover letter generation failed: {e}")
        cover_letter = f"Dear Hiring Manager,\n\n"
        cover_letter += f"I am writing to express my strong interest in the {job_title} position at {company_name}.\n\n"
        cover_letter += f"{profile.summary if profile and profile.summary else 'I am a dedicated professional with a passion for delivering quality work and continuous learning.'}\n\n"
        cover_letter += f"I am excited about the opportunity to contribute to {company_name} and would welcome the chance to discuss how I can add value to your team.\n\n"
        cover_letter += f"Best regards,\n{user.name}"
        return cover_letter
