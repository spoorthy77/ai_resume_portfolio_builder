"""
Enhanced Resume templates with AI optimization and MS Word standard formatting
Integrates AIResumeEnhancer for professional content generation and MS Word compatibility
"""
try:
    from .ai_resume_enhancer import AIResumeEnhancer
except ImportError:
    from ai_resume_enhancer import AIResumeEnhancer


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
        """Professional/Formal resume template - ATS-friendly, traditional format
        
        Format: Calibri 11pt, 1.15 spacing, centered margins
        Optimized for: Corporate, Finance, Business roles
        Section Order: Summary → Experience → Skills → Education → Projects
        """
        return AIResumeEnhancer.format_resume_ms_word_standard('professional', user, profile)
    
    @staticmethod
    def modern(user, profile):
        """Modern/Creative resume template - Contemporary design, achievement-focused
        
        Format: Segoe UI 11pt, visual elements, colored accents
        Optimized for: Creative, Marketing, Tech roles
        Section Order: Summary → Skills → Experience → Projects → Education
        """
        return AIResumeEnhancer.format_resume_ms_word_standard('modern', user, profile)
    
    @staticmethod
    def simple(user, profile):
        """Simple/Minimal resume template - Clean, scannable, ATS-optimized
        
        Format: Arial 10pt, 1.0 spacing, minimal styling
        Optimized for: All industries (maximum ATS compatibility)
        Section Order: Summary → Experience → Education → Skills → Projects
        """
        return AIResumeEnhancer.format_resume_ms_word_standard('simple', user, profile)
    
    @staticmethod
    def technical(user, profile):
        """Technical-focused resume template - Skills-first, tech industry optimized
        
        Format: Consolas 10pt, code-style formatting
        Optimized for: Software Development, Engineering, Tech roles
        Section Order: Summary → SKILLS FIRST → Experience → Projects → Education
        """
        return AIResumeEnhancer.format_resume_ms_word_standard('technical', user, profile)
    
    @staticmethod
    def academic(user, profile):
        """Academic-focused resume template - CV format, research-oriented
        
        Format: Times New Roman 12pt, 1.5 spacing, academic style
        Optimized for: Academic, Research, Education roles
        Section Order: EDUCATION FIRST → Experience → Projects → Skills → Summary
        """
        return AIResumeEnhancer.format_resume_ms_word_standard('academic', user, profile)
    
    @staticmethod
    def detailed(user, profile):
        """Detailed/Comprehensive resume template - Extended format, all sections expanded
        
        Format: Garamond 11pt, 1.15 spacing, comprehensive sections
        Optimized for: Executive, Senior roles, detailed accomplishments
        Section Order: Summary → Experience → Skills → Projects → Education
        """
        return AIResumeEnhancer.format_resume_ms_word_standard('detailed', user, profile)
    
    @staticmethod
    def get_all_templates():
        """Return available template names and descriptions with AI optimization info
        
        Returns:
            dict: Template information including names, descriptions, fonts, sizes, and AI features
        """
        templates = AIResumeEnhancer.list_all_formats()
        
        template_dict = {}
        for template in templates:
            template_dict[template['id']] = {
                'name': template['name'],
                'description': template['description'],
                'font': template['font'],
                'size': template['size'],
                'icon': get_template_icon(template['id']),
                'ai_features': get_ai_features_for_template(template['id'])
            }
        
        return template_dict
    
    @staticmethod
    def generate_from_template(template_name, user, profile):
        """Generate resume from specified template with AI enhancement
        
        AI Features Applied:
        - Smart headline enhancement by industry
        - Summary optimization with industry-specific language
        - Skill categorization (Technical, Professional, Additional)
        - Experience bullet points with impact metrics
        - Professional formatting per MS Word standards
        - ATS optimization where applicable
        
        Args:
            template_name: Name of the template to use
            user: User object with name and email
            profile: Profile object with all fields
            
        Returns:
            str: Generated resume string with AI enhancements
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
        """Export resume as MS Word (.docx) file with professional formatting
        
        Generates professionally formatted Word documents with:
        - Proper margins and spacing per template specifications
        - Professional font selection (Calibri, Segoe UI, Arial, etc.)
        - Color-coded headers matching template style
        - ATS-optimized formatting for maximum compatibility
        
        Args:
            template_name: Template to use
            user: User object with name and email
            profile: Profile object with all content
            output_path: Path where .docx file will be saved
            
        Returns:
            bool: True if export successful, False otherwise
        """
        return AIResumeEnhancer.generate_word_document(
            template_name.lower(),
            user,
            profile,
            output_path
        )
    
    @staticmethod
    def get_template_specs(template_name):
        """Get detailed format specifications for a template
        
        Args:
            template_name: Template name
            
        Returns:
            dict: Format specifications including font, size, margins, colors, section order
        """
        return AIResumeEnhancer.get_format_specs(template_name.lower())
    
    @staticmethod
    def enhance_content(content_type, text, industry='technology'):
        """Apply AI enhancement to resume content
        
        Args:
            content_type: Type of content ('headline', 'summary', 'experience', 'bullet')
            text: Content to enhance
            industry: Industry type for context-aware enhancement
            
        Returns:
            str: Enhanced content
        """
        if content_type == 'headline':
            return AIResumeEnhancer.enhance_headline(text, industry)
        elif content_type == 'summary':
            return AIResumeEnhancer.enhance_summary(text, industry)
        elif content_type == 'experience' or content_type == 'bullet':
            return AIResumeEnhancer.enhance_experience_bullets(text)
        else:
            return text
    
    @staticmethod
    def categorize_skills(skills_str):
        """Merge and categorize all skills into a single Technical Skills list
        
        Combines all user-provided skills into one unified Technical Skills category.
        Removes duplicates while preserving order.
        
        Args:
            skills_str: Comma-separated skills string
            
        Returns:
            dict: Skills organized with single 'Technical Skills' key containing merged list
        """
        return AIResumeEnhancer.categorize_skills(skills_str)


def get_template_icon(template_id):
    """Get emoji icon for template"""
    icons = {
        'professional': '💼',
        'modern': '🎨',
        'simple': '📋',
        'technical': '⚙️',
        'academic': '🎓',
        'detailed': '📄'
    }
    return icons.get(template_id, '📃')


def get_ai_features_for_template(template_id):
    """Get AI features enabled for a specific template"""
    features = {
        'professional': ['Smart headlines', 'Summary optimization', 'Skill categorization', 'ATS optimized'],
        'modern': ['Visual enhancement', 'Skill grouping', 'Achievement focus', 'Professional polish'],
        'simple': ['ATS optimization', 'Minimal styling', 'Scannable layout', 'Clean formatting'],
        'technical': ['Skills-first priority', 'Tech stack emphasis', 'Code-style formatting', 'Impact metrics'],
        'academic': ['Academic language', 'Research focus', 'CV formatting', 'Educational priority'],
        'detailed': ['Comprehensive sections', 'Executive polish', 'Achievement emphasis', 'Full detail preservation']
    }
    return features.get(template_id, [])
