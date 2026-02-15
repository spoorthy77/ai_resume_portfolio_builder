"""
Enhanced Resume templates with AI optimization and MS Word standard formatting
Integrates AIResumeEnhancer for professional content generation
"""
from .ai_resume_enhancer import AIResumeEnhancer


class ResumeTemplates:
    """Collection of AI-enhanced resume templates matching MS Word standards"""
    
    @staticmethod
    def _enhance_bullets(text):
        """Convert text to professional bullet points"""
        if not text:
            return text
        return AIResumeEnhancer.enhance_experience_bullets(text)
    
    @staticmethod
    def professional(user, profile):
        """Professional/Formal resume template - ATS-friendly, traditional format"""
        return AIResumeEnhancer.format_resume_ms_word_standard('professional', user, profile)
    
    @staticmethod
    def modern(user, profile):
        """Modern/Creative resume template - Contemporary design, achievement-focused"""
        return AIResumeEnhancer.format_resume_ms_word_standard('modern', user, profile)
    
    @staticmethod
    def simple(user, profile):
        """Simple/Minimal resume template - Clean, scannable, ATS-optimized"""
        return AIResumeEnhancer.format_resume_ms_word_standard('simple', user, profile)
    
    @staticmethod
    def technical(user, profile):
        """Technical-focused resume template - Skills-first, tech industry optimized"""
        return AIResumeEnhancer.format_resume_ms_word_standard('technical', user, profile)
    
    @staticmethod
    def academic(user, profile):
        """Academic-focused resume template - CV format, research-oriented"""
        return AIResumeEnhancer.format_resume_ms_word_standard('academic', user, profile)
    
    @staticmethod
    def detailed(user, profile):
        """Detailed/Comprehensive resume template - Extended format, all sections expanded"""
        return AIResumeEnhancer.format_resume_ms_word_standard('detailed', user, profile)
    
    @staticmethod
    def get_all_templates():
        """Return available template names and descriptions"""
        templates = AIResumeEnhancer.list_all_formats()
        
        template_dict = {}
        for template in templates:
            template_dict[template['id']] = {
                'name': template['name'],
                'description': template['description'],
                'font': template['font'],
                'size': template['size']
            }
        
        return template_dict
    
    @staticmethod
    def generate_from_template(template_name, user, profile):
        """Generate resume from specified template with AI enhancement
        
        Args:
            template_name: Name of the template to use
            user: User object with name and email
            profile: Profile object with all fields
            
        Returns:
            Generated resume string
        """
        templates = {
            'professional': ResumeTemplates.professional,
            'modern': ResumeTemplates.modern,
            'simple': ResumeTemplates.simple,
            'technical': ResumeTemplates.technical,
            'academic': ResumeTemplates.academic,
            'detailed': ResumeTemplates.detailed
        }
        
        template_func = templates.get(template_name.lower(), ResumeTemplates.professional)
        return template_func(user, profile)
    
    @staticmethod
    def export_as_docx(template_name, user, profile, output_path):
        """Export resume as MS Word (.docx) file with proper formatting"""
        return AIResumeEnhancer.generate_word_document(
            template_name.lower(),
            user,
            profile,
            output_path
        )
    
    @staticmethod
    def get_template_specs(template_name):
        """Get detailed format specifications for a template"""
        return AIResumeEnhancer.get_format_specs(template_name.lower())
