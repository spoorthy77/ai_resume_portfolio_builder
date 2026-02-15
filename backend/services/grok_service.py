"""
Grok API Service for AI-Powered Resume Generation
Integrates with Grok API for high-quality, ATS-optimized resume generation
"""
import requests
from backend.config import Config

GROK_URL = "https://api.x.ai/v1/chat/completions"
AI_API_KEY = Config.GROQ_API_KEY


def build_resume_prompt(profile_data):
    """
    Build a high-quality resume generation prompt optimized for ATS and professional standards.
    
    Args:
        profile_data: Dictionary containing user profile information
        
    Returns:
        Formatted prompt string for Grok API
    """
    return f"""
You are a professional resume writer and ATS optimization expert.

Your task is to generate a CONCISE, clean, modern, ATS-friendly resume that FITS ON ONE PAGE.

CRITICAL INSTRUCTIONS:
- Output MUST fit on ONE page only
- Follow the EXACT section titles given below
- Keep section names in ALL CAPS
- Do NOT change section order
- Do NOT add extra sections
- Do NOT invent information
- Use ONLY provided data
- Use professional tone with strong action verbs
- Be CONCISE - 2-3 lines per section maximum
- Use bullet points for lists (start with •)
- Format with clear spacing between sections
- Output ONLY resume content - NO explanations, NO markdown, NO commentary

========================

PROFESSIONAL SUMMARY
Write 2-3 powerful professional lines (no bullet points):
{profile_data.get("headline", "")}
{profile_data.get("summary", "")}

EDUCATION
List only degree, institution, and graduation year:
{" | ".join(profile_data.get("education", []))}

TECHNICAL SKILLS
Format as category: skill1, skill2, skill3 (use bullet points):
{", ".join(profile_data.get("skills", []))}

PROJECTS
For each project: Name – Brief description in 1 line with key technology:
{" | ".join(profile_data.get("projects", []))}

WORK EXPERIENCE
Format: Role – Company (Years) - 2 bullet points on achievements:
{" | ".join(profile_data.get("experience", []))}

========================

REMEMBER:
- CONCISE and PROFESSIONAL
- Fits on ONE page
- No extra spacing
- No markdown
- Resume content ONLY
"""


def generate_resume_with_grok(profile_data):
    """
    Generate a professional ATS-optimized resume using Grok API.
    
    Args:
        profile_data: Dictionary containing user profile information
        
    Returns:
        Generated resume content as string
        
    Raises:
        Exception: If API call fails
    """
    prompt = build_resume_prompt(profile_data)

    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "grok-2-latest",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post(GROK_URL, json=payload, headers=headers, timeout=30)

        if response.status_code != 200:
            raise Exception(f"Grok API Error: {response.status_code} - {response.text}")

        return response.json()["choices"][0]["message"]["content"]
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to connect to Grok API: {str(e)}")
    except (KeyError, ValueError) as e:
        raise Exception(f"Failed to parse Grok API response: {str(e)}")


def build_cover_letter_prompt(profile_data, job_data):
    """
    Build a professional cover letter generation prompt.
    
    Args:
        profile_data: Dictionary containing user profile information
        job_data: Dictionary containing job information
        
    Returns:
        Formatted prompt string for Grok API
    """
    return f"""
You are a professional cover letter writer specializing in ATS-optimized applications.

Your task is to generate a compelling, professional cover letter that highlights the candidate's strengths and matches the job requirements.

IMPORTANT RULES:
- Do NOT invent qualifications.
- Use only the data provided.
- Write in a professional, engaging tone.
- Optimize for ATS by using relevant keywords from job description.
- Use action verbs and specific achievements.
- Keep it concise (3-4 paragraphs).
- Do not include explanations or commentary.
- Output ONLY the cover letter.

CANDIDATE DATA:

Name: {profile_data.get("name", "")}
Headline: {profile_data.get("headline", "")}
Summary: {profile_data.get("summary", "")}
Skills: {", ".join(profile_data.get("skills", []))}
Experience: {" | ".join(profile_data.get("experience", []))}

JOB DATA:

Position: {job_data.get("position", "")}
Company: {job_data.get("company", "")}
Description: {job_data.get("description", "")}

Now generate the cover letter.
"""


def generate_cover_letter_with_grok(profile_data, job_data):
    """
    Generate a professional cover letter using Grok API.
    
    Args:
        profile_data: Dictionary containing user profile information
        job_data: Dictionary containing job information
        
    Returns:
        Generated cover letter content as string
        
    Raises:
        Exception: If API call fails
    """
    prompt = build_cover_letter_prompt(profile_data, job_data)

    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "grok-2-latest",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post(GROK_URL, json=payload, headers=headers, timeout=30)

        if response.status_code != 200:
            raise Exception(f"Grok API Error: {response.status_code} - {response.text}")

        return response.json()["choices"][0]["message"]["content"]
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to connect to Grok API: {str(e)}")
    except (KeyError, ValueError) as e:
        raise Exception(f"Failed to parse Grok API response: {str(e)}")


def build_resume_optimization_prompt(resume_text, job_description):
    """
    Build a resume optimization prompt to enhance resume for a specific job description.
    
    Args:
        resume_text: The original resume content as string
        job_description: The job description to optimize against as string
        
    Returns:
        Formatted prompt string for Grok API
    """
    return f"""
You are an ATS optimization specialist and technical recruiter.

Your task is to improve the resume so it better matches the provided Job Description.

RULES:
- Do NOT add fake experience.
- Only rephrase and reorganize existing content.
- Inject relevant keywords from the Job Description naturally.
- Maintain honesty and accuracy.
- Improve impact using strong action verbs.
- Ensure ATS compatibility.
- Keep formatting professional and clean.

OUTPUT:
Return ONLY the improved resume.
Do not include explanations.

ORIGINAL RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Now generate the optimized resume.
"""


def build_resume_scoring_prompt(resume_text, job_description):
    """
    Build a resume scoring prompt to analyze ATS match percentage and provide improvement suggestions.
    
    Args:
        resume_text: The resume content as string
        job_description: The job description to score against as string
        
    Returns:
        Formatted prompt string for Grok API
    """
    return f"""
You are an Applicant Tracking System (ATS) analyzer.

Compare the resume against the Job Description and provide:

1. Match Score (0–100%)
2. Missing Keywords
3. Strengths Found
4. Weak Areas
5. Specific Improvements to Increase Score

Be precise and professional.
Do NOT rewrite the resume.
This is an evaluation report.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""


def build_portfolio_prompt(profile_data):
    """
    Build a professional portfolio website copywriting prompt.
    
    Args:
        profile_data: Dictionary containing user profile information
        
    Returns:
        Formatted prompt string for Grok API
    """
    return f"""
You are a professional portfolio website copywriter.

Generate content for a personal developer portfolio website.

SECTIONS REQUIRED:
- Hero Introduction
- About Me
- Skills Overview
- Featured Projects (descriptive)
- Experience Summary
- Contact Section Text

Keep tone modern, confident, and professional.
Do NOT fabricate information.

USER DATA:
Headline: {profile_data['headline']}
Summary: {profile_data['summary']}
Skills: {", ".join(profile_data['skills'])}
Projects: {" | ".join(profile_data['projects'])}
Experience: {" | ".join(profile_data['experience'])}
Education: {" | ".join(profile_data['education'])}
"""


def generate_portfolio_with_grok(profile_data):
    """
    Generate a professional portfolio using Grok API.
    
    Args:
        profile_data: Dictionary containing user profile information
        
    Returns:
        Generated portfolio content as string
        
    Raises:
        Exception: If API call fails
    """
    prompt = build_portfolio_prompt(profile_data)

    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "grok-2-latest",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post(GROK_URL, json=payload, headers=headers, timeout=30)

        if response.status_code != 200:
            raise Exception(f"Grok API Error: {response.status_code} - {response.text}")

        return response.json()["choices"][0]["message"]["content"]
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to connect to Grok API: {str(e)}")
    except (KeyError, ValueError) as e:
        raise Exception(f"Failed to parse Grok API response: {str(e)}")


def build_resume_optimization_prompt(resume_text, job_description):
    """
    Build a resume optimization prompt to match job description.
    
    Optimizes the resume for a specific job by injecting relevant keywords
    and reorganizing content to better align with job requirements.
    
    Args:
        resume_text: Current resume content
        job_description: Job description to optimize against
        
    Returns:
        Formatted prompt string for Grok API
    """
    return f"""
You are an ATS optimization specialist and technical recruiter.

Your task is to improve the resume so it better matches the provided Job Description.

RULES:
- Do NOT add fake experience.
- Only rephrase and reorganize existing content.
- Inject relevant keywords from the Job Description naturally.
- Maintain honesty and accuracy.
- Improve impact using strong action verbs.
- Ensure ATS compatibility.
- Keep formatting professional and clean.

OUTPUT:
Return ONLY the improved resume.
Do not include explanations.

ORIGINAL RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Now generate the optimized resume.
"""


def optimize_resume_with_grok(resume_text, job_description):
    """
    Optimize a resume against a specific job description using Grok API.
    
    Injects relevant keywords and rephrases content to better match job requirements
    while maintaining accuracy and honesty.
    
    Args:
        resume_text: Current resume content
        job_description: Job description to optimize against
        
    Returns:
        Optimized resume content as string
        
    Raises:
        Exception: If API call fails
    """
    prompt = build_resume_optimization_prompt(resume_text, job_description)

    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "grok-2-latest",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post(GROK_URL, json=payload, headers=headers, timeout=30)

        if response.status_code != 200:
            raise Exception(f"Grok API Error: {response.status_code} - {response.text}")

        return response.json()["choices"][0]["message"]["content"]
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to connect to Grok API: {str(e)}")
    except (KeyError, ValueError) as e:
        raise Exception(f"Failed to parse Grok API response: {str(e)}")


def build_pdf_format_prompt(resume_text):
    """
    Build a resume PDF formatting prompt for clean PDF export.
    
    Args:
        resume_text: The resume content as string
        
    Returns:
        Formatted prompt string for Grok API
    """
    return f"""
Format the following resume into a clean, compact layout suitable for PDF export.

RULES:
- Use clear section headings.
- Keep spacing balanced.
- Avoid long paragraphs.
- Maintain ATS readability.
- Do NOT change meaning.

RESUME:
{resume_text}
"""
