"""
AI-powered routes for resume, cover letter, and portfolio generation
"""
from flask import Blueprint, request, jsonify, session, Response
from backend.routes.auth_routes import users
from backend.services.resume_generator import generate_resume
from backend.services.cover_letter_generator import generate_cover_letter
from backend.services.portfolio_generator import generate_portfolio
from backend.services.resume_templates import ResumeTemplates
from backend.services.resume_optimizer import ResumeOptimizer
from backend.services.resume_exporter import ResumeExporter

ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')

ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')

class SimpleUser:
    def __init__(self, user_data, profile_data):
        self.id = user_data['id']
        self.name = user_data['name']
        self.email = user_data['email']
        self.profile = SimpleProfile(profile_data) if profile_data else None

class SimpleProfile:
    def __init__(self, data):
        self.headline = data.get('headline', '')
        self.phone = data.get('phone', '')
        self.linkedin = data.get('linkedin', '')
        self.github = data.get('github', '')
        self.email = data.get('email', '')
        self.leetcode = data.get('leetcode', '')
        self.other_links = data.get('other_links', '')
        self.summary = data.get('summary', '')
        self.skills = data.get('skills', '')
        self.projects = data.get('projects', '')
        self.experience = data.get('experience', '')
        self.education = data.get('education', '')
        self.dob = data.get('dob', '')
        self.languages = data.get('languages', '')
        self.hobbies = data.get('hobbies', '')

def get_user_from_session():
    user_id = session.get('user_id')
    if not user_id:
        return None
    # Find user by id
    for email, user_data in users.items():
        if user_data['id'] == user_id:
            profile_data = session.get('profile', {})
            return SimpleUser(user_data, profile_data)
    return None

@ai_bp.route('/templates', methods=['GET'])
def get_templates():
    """Get available resume templates"""
    templates = ResumeTemplates.get_all_templates()
    return jsonify({'templates': templates}), 200

@ai_bp.route('/export-formats', methods=['GET'])
def get_export_formats():
    """Get supported resume export formats"""
    formats = ResumeExporter.get_supported_formats()
    return jsonify({'formats': formats}), 200

@ai_bp.route('/generate-resume', methods=['POST'])
def generate_resume_endpoint():
    """Generate resume using AI with template selection and export format"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user = get_user_from_session()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    try:
        data = request.get_json(silent=True) or {}
        export_format = data.get('format', 'txt').lower()
        template_name = data.get('template', 'professional')

        # Validate format
        supported_formats = [f['format'] for f in ResumeExporter.get_supported_formats()]
        if export_format not in supported_formats:
            export_format = 'txt'

        # Get profile data
        profile_data = session.get('profile', {})

        # Generate resume in requested format
        resume_content, content_type = ResumeExporter.export_resume(
            user, profile_data, export_format, template_name
        )

        # For file downloads, return as attachment
        if export_format in ['pdf', 'docx']:
            format_info = next(f for f in ResumeExporter.get_supported_formats() if f['format'] == export_format)
            filename = f"resume_{user.name.lower().replace(' ', '_')}{format_info['extension']}"

            response = Response(
                resume_content,
                mimetype=content_type,
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )
            return response
        elif export_format == 'html':
            # For HTML format, return as JSON with HTML content
            html_content = resume_content.decode('utf-8')
            return jsonify({'resume': html_content, 'format': 'html'}), 200
        else:
            # For text format, return as JSON
            resume_text = resume_content.decode('utf-8')
            return jsonify({'resume': resume_text}), 200

    except Exception as e:
        return jsonify({'error': f'Failed to generate resume: {str(e)}'}), 500

@ai_bp.route('/generate-cover-letter', methods=['POST'])
def generate_cover_letter_endpoint():
    """Generate cover letter using AI"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = get_user_from_session()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    try:
        data = request.get_json(silent=True) or {}
        cover_letter = generate_cover_letter(user, data)
        return jsonify({'cover_letter': cover_letter}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to generate cover letter: {str(e)}'}), 500

@ai_bp.route('/generate-portfolio', methods=['POST'])
def generate_portfolio_endpoint():
    """Generate portfolio using AI"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = get_user_from_session()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    try:
        data = request.get_json(silent=True) or {}
        portfolio = generate_portfolio(user, data)
        return jsonify({'portfolio': portfolio}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to generate portfolio: {str(e)}'}), 500

@ai_bp.route('/analyze-resume', methods=['POST'])
def analyze_resume_endpoint():
    """Analyze resume against job description
    
    Request body:
    {
        "job_description": "Job description text",
        "resume_text": "Resume text (optional, fetched from profile if not provided)"
    }
    
    Returns:
    {
        "match_score": 85,
        "missing_keywords": ["keyword1", "keyword2"],
        "overlapping_keywords": ["keyword1", "keyword2"],
        "suggestions": ["suggestion1", "suggestion2"]
    }
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = get_user_from_session()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    try:
        data = request.get_json(silent=True) or {}
        job_description = data.get('job_description', '').strip()
        
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400
        
        # Get resume text from request or build from user profile
        resume_text = data.get('resume_text', '').strip()
        
        if not resume_text and user.profile:
            # Build resume text from profile data
            profile = user.profile
            resume_parts = [
                f"Name: {user.name}",
                f"Headline: {profile.headline or ''}",
                f"Summary: {profile.summary or ''}",
                f"Skills: {profile.skills or ''}",
                f"Projects: {profile.projects or ''}",
                f"Education: {profile.education or ''}"
            ]
            resume_text = '\n'.join([part for part in resume_parts if part])
        
        if not resume_text:
            return jsonify({'error': 'Resume content not found. Please complete your profile first.'}), 400
        
        # Analyze resume
        analysis_result = ResumeOptimizer.calculate_match_score(resume_text, job_description)
        
        return jsonify(analysis_result), 200
    except Exception as e:
        return jsonify({'error': f'Failed to analyze resume: {str(e)}'}), 500