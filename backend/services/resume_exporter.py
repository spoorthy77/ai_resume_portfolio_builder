"""
Resume export service for generating resumes in multiple formats
"""
import io
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from backend.services.resume_templates import ResumeTemplates

class ResumeExporter:
    """Service for exporting resumes in multiple formats"""

    @staticmethod
    def export_resume(user, profile_data, format_type='txt', template_name='professional'):
        """
        Export resume in specified format

        Args:
            user: User object
            profile_data: Profile data dictionary
            format_type: 'txt', 'pdf', 'docx', 'html'
            template_name: Template name

        Returns:
            File content as bytes and content type
        """
        if format_type.lower() == 'pdf':
            return ResumeExporter._generate_pdf(user, profile_data, template_name)
        elif format_type.lower() == 'docx':
            return ResumeExporter._generate_docx(user, profile_data, template_name)
        elif format_type.lower() == 'html':
            return ResumeExporter._generate_html(user, profile_data, template_name)
        else:  # default to txt
            return ResumeExporter._generate_txt(user, profile_data, template_name)

    @staticmethod
    def _generate_txt(user, profile_data, template_name):
        """Generate plain text resume"""
        from backend.services.resume_templates import ResumeTemplates

        # Create a simple user object for template compatibility
        class SimpleUser:
            def __init__(self, user_obj, profile_data):
                self.name = getattr(user_obj, 'name', profile_data.get('name', '[Your Name]'))
                self.email = getattr(user_obj, 'email', profile_data.get('email', '[Your Email]'))

        class SimpleProfile:
            def __init__(self, data, user_obj):
                self.headline = data.get('headline', '')
                self.phone = data.get('phone', '[Your Phone]')
                self.linkedin = data.get('linkedin', '')
                self.github = data.get('github', '')
                self.email = data.get('email', getattr(user_obj, 'email', '[Your Email]'))
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

        simple_user = SimpleUser(user, profile_data)
        simple_profile = SimpleProfile(profile_data, user)

        resume_text = ResumeTemplates.generate_from_template(template_name, simple_user, simple_profile)
        return resume_text.encode('utf-8'), 'text/plain'

    @staticmethod
    def _generate_docx(user, profile_data, template_name):
        """Generate MS Word (.docx) resume"""
        from backend.services.resume_templates import ResumeTemplates
        import tempfile
        import os

        class SimpleUser:
            def __init__(self, user_obj, profile_data):
                self.name = getattr(user_obj, 'name', profile_data.get('name', '[Your Name]'))
                self.email = getattr(user_obj, 'email', profile_data.get('email', '[Your Email]'))

        class SimpleProfile:
            def __init__(self, data, user_obj):
                self.headline = data.get('headline', '')
                self.phone = data.get('phone', '[Your Phone]')
                self.linkedin = data.get('linkedin', '')
                self.github = data.get('github', '')
                self.email = data.get('email', getattr(user_obj, 'email', '[Your Email]'))
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

        simple_user = SimpleUser(user, profile_data)
        simple_profile = SimpleProfile(profile_data, user)

        # Create temporary file path
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"resume_{template_name}.docx")
        
        # Use ResumeTemplates/AIResumeEnhancer to generate DOCX
        ResumeTemplates.export_as_docx(template_name, simple_user, simple_profile, temp_path)
        
        # Read the file content
        with open(temp_path, 'rb') as f:
            content = f.read()
            
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        return content, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

    @staticmethod
    def _generate_pdf(user, profile_data, template_name):
        """
        Generate a single-page PDF resume using an AI auto-fit engine.
        The layout is dynamically adjusted to ensure all content fits on exactly one page.
        """
        from backend.services.ai_content_compressor import AIContentCompressor

        class SimpleUser:
            def __init__(self, user_obj, profile_data):
                self.name = getattr(user_obj, 'name', profile_data.get('name', '[Your Name]'))
                self.email = getattr(user_obj, 'email', profile_data.get('email', '[Your Email]'))

        class SimpleProfile:
            def __init__(self, data, user_obj):
                self.headline = data.get('headline', '')
                self.phone = data.get('phone', '[Your Phone]')
                self.linkedin = data.get('linkedin', '')
                self.github = data.get('github', '')
                self.email = data.get('email', getattr(user_obj, 'email', '[Your Email]'))
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

        simple_user = SimpleUser(user, profile_data)
        simple_profile = SimpleProfile(profile_data, user)

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            topMargin=0.5 * inch,
            bottomMargin=0.5 * inch,
            leftMargin=0.5 * inch,
            rightMargin=0.5 * inch
        )
        
        usable_height = doc.height
        
        # Initial parameters for the auto-fit engine
        font_size = 11
        leading = 14
        section_spacing = 6
        compressed_summary = False
        compressed_projects = False

        for iteration in range(10):
            # Generate resume text from template
            resume_text = ResumeTemplates.generate_from_template(template_name, simple_user, simple_profile)
            resume_lines = resume_text.split('\n')

            # Define styles based on current scaling parameters
            styles = ResumeExporter._get_pdf_styles(font_size, leading, section_spacing)
            
            # Build the story
            story = []
            ResumeExporter._build_pdf_story_flow(
                story, resume_lines, simple_profile,
                styles['NameStyle'], styles['HeadlineStyle'], styles['HeadingStyle'],
                styles['SummaryStyle'], styles['NormalStyle'], styles['ProjectTitleStyle'],
                styles['ProjectDescriptionStyle'], styles['BulletStyle'], styles['CenteredNormal'], doc.width
            )

            # Estimate total height by simulating content layout
            total_height = 0
            for flowable in story:
                w, h = flowable.wrap(doc.width, usable_height)
                total_height += h

            # Check if content fits
            if total_height <= usable_height:
                # Check if utilization is good (95-99%)
                utilization = total_height / usable_height
                if utilization >= 0.95:
                    break  # Perfect fit found
                elif utilization >= 0.90:
                    break  # Good enough fit
                # If too much whitespace (<90%), don't increase spacing to avoid overflow

            # PRIORITY 1: Reduce section spacing
            if section_spacing > 2:
                section_spacing -= 0.5
                continue

            # PRIORITY 2: Reduce paragraph spacing
            # Handled in styles generation, reduce spaceAfter values
            if section_spacing > 2:
                section_spacing -= 0.5
                continue

            # PRIORITY 3: Reduce leading
            if leading > font_size + 1:
                leading -= 0.5
                continue

            # PRIORITY 4: Reduce font size
            if font_size > 8:
                font_size -= 0.5
                leading = font_size + 1.5  # Maintain minimum leading
                continue

            # PRIORITY 5: Compress summary to max 3 lines
            if not compressed_summary and simple_profile.summary:
                simple_profile.summary = AIContentCompressor.compress_summary(simple_profile.summary)
                compressed_summary = True
                continue

            # PRIORITY 6: Limit projects to 2 bullets each
            if not compressed_projects and simple_profile.projects:
                simple_profile.projects = AIContentCompressor.compress_projects(simple_profile.projects)
                compressed_projects = True
                continue

            # If we reach here, content should fit
            break

        # Final build with optimized styles
        story = []
        resume_text = ResumeTemplates.generate_from_template(template_name, simple_user, simple_profile)
        resume_lines = resume_text.split('\n')
        styles = ResumeExporter._get_pdf_styles(font_size, leading, section_spacing)
        
        ResumeExporter._build_pdf_story_flow(
            story, resume_lines, simple_profile,
            styles['NameStyle'], styles['HeadlineStyle'], styles['HeadingStyle'],
            styles['SummaryStyle'], styles['NormalStyle'], styles['ProjectTitleStyle'],
            styles['ProjectDescriptionStyle'], styles['BulletStyle'], styles['CenteredNormal'], doc.width
        )

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue(), 'application/pdf'

    @staticmethod
    def _get_pdf_styles(font_size, leading, section_spacing):
        """Returns a dictionary of ParagraphStyle objects for PDF generation."""
        styles = getSampleStyleSheet()
        
        base_font_name = 'Times-Roman'
        bold_font_name = 'Times-Bold'
        
        return {
            'NameStyle': ParagraphStyle(
                'NameStyle', parent=styles['Normal'], fontName=bold_font_name,
                fontSize=16, leading=19, textColor=colors.HexColor("#1F4E79"),
                alignment=TA_CENTER, spaceAfter=6
            ),
            'HeadlineStyle': ParagraphStyle(
                'HeadlineStyle', parent=styles['Normal'], fontName=base_font_name,
                fontSize=12, leading=14, alignment=TA_CENTER, spaceAfter=4
            ),
            'HeadingStyle': ParagraphStyle(
                'HeadingStyle', parent=styles['Normal'], fontName=bold_font_name,
                fontSize=font_size + 1, leading=leading + 1, textColor=colors.HexColor("#1F4E79"),
                spaceBefore=section_spacing, spaceAfter=3
            ),
            'SummaryStyle': ParagraphStyle(
                'SummaryStyle', parent=styles['Normal'], fontName=base_font_name,
                fontSize=font_size, leading=leading, spaceAfter=3
            ),
            'NormalStyle': ParagraphStyle(
                'NormalStyle', parent=styles['Normal'], fontName=base_font_name,
                fontSize=font_size, leading=leading, spaceAfter=2
            ),
            'ProjectTitleStyle': ParagraphStyle(
                'ProjectTitleStyle', parent=styles['Normal'], fontName=bold_font_name,
                fontSize=font_size, leading=leading, textColor=colors.black,
                spaceBefore=4, spaceAfter=2
            ),
            'ProjectDescriptionStyle': ParagraphStyle(
                'ProjectDescriptionStyle', parent=styles['Normal'], fontName=base_font_name,
                fontSize=font_size, leading=leading, bulletText='•', leftIndent=12,
                spaceAfter=3
            ),
            'BulletStyle': ParagraphStyle(
                'BulletStyle', parent=styles['Normal'], fontName=base_font_name,
                fontSize=font_size - 1, leading=leading - 1, leftIndent=15,
                bulletIndent=5, spaceAfter=1
            ),
            'CenteredNormal': ParagraphStyle(
                'CenteredNormal', parent=styles['Normal'], fontName=base_font_name,
                fontSize=font_size, leading=leading, alignment=TA_CENTER,
                textColor=colors.HexColor("#4472C4")
            )
        }
    
    @staticmethod
    def _build_pdf_story_flow(story, resume_lines, profile, name_style, headline_style, heading_style,
                             summary_style, normal_style, project_title_style, project_description_style, 
                             bullet_style, centered_normal_style, usable_width):
        """Build the PDF story with structured content."""
        section_mappings = {
            'PROFESSIONAL SUMMARY': 'Professional Summary', 'EDUCATION': 'Education',
            'TECHNICAL SKILLS': 'Technical Skills', 'PROJECTS & ACHIEVEMENTS': 'Projects & Achievements',
            'PROJECTS': 'Projects & Achievements',
            'ADDITIONAL INFORMATION': 'Additional Information', 'EXPERIENCE': 'Experience',
            'PROFESSIONAL EXPERIENCE': 'Professional Experience', 'WORK EXPERIENCE': 'Work Experience',
            'SKILLS': 'Skills', 'CERTIFICATIONS': 'Certifications',
            'LANGUAGES': 'Languages', 'HOBBIES': 'Hobbies'
        }

        name_line = resume_lines[0].title() if resume_lines else '[Your Name]'
        headline_line = resume_lines[1] if len(resume_lines) > 1 else ''
        contact_line = resume_lines[2] if len(resume_lines) > 2 else ''

        story.append(Paragraph(name_line.strip(), name_style))
        if headline_line.strip():
            story.append(Paragraph(headline_line.strip(), headline_style))

        contact_parts = []
        for part in contact_line.split('|'):
            part = part.strip()
            if 'LinkedIn' in part and profile.linkedin:
                contact_parts.append(f'<a href="https://{profile.linkedin}">LinkedIn</a>')
            elif 'GitHub' in part and profile.github:
                contact_parts.append(f'<a href="https://{profile.github}">GitHub</a>')
            elif 'LeetCode' in part and profile.leetcode:
                contact_parts.append(f'<a href="https://{profile.leetcode}">LeetCode</a>')
            else:
                contact_parts.append(part)
        if contact_parts:
            story.append(Paragraph(' | '.join(contact_parts), centered_normal_style))

        story.append(Spacer(1, 7))

        i = 3
        current_section = None
        while i < len(resume_lines):
            line = resume_lines[i]
            if not line.strip() or '─' in line:
                i += 1
                continue

            if line.isupper() and len(line) > 3:
                mixed_case_heading = section_mappings.get(line.strip(), line.strip().title())
                story.append(Paragraph(mixed_case_heading, heading_style))
                story.append(HRFlowable(width=usable_width, thickness=0.5, color=colors.HexColor("#1F4E79"), spaceBefore=0, spaceAfter=normal_style.spaceAfter))
                current_section = line.strip()
            elif current_section in ['PROJECTS', 'PROJECTS & ACHIEVEMENTS']:
                # Special handling for projects: separate titles from descriptions
                clean_line = line.strip()
                
                # Check if this is a project title (marked with __TITLE__)
                if '__TITLE__' in clean_line:
                    # Extract title and remove marker
                    title_text = clean_line.replace('__TITLE__', '').strip()
                    # Remove any leading bullet points or numbers if present
                    title_text = re.sub(r'^[0-9]+\s+', '', title_text)
                    title_text = title_text.lstrip('-•').strip()
                    # Add title WITHOUT bullet
                    story.append(Paragraph(title_text, project_title_style))
                elif clean_line.startswith('•') or clean_line.startswith('-'):
                    # This is a project description with bullet
                    desc_text = clean_line.lstrip('-•').strip()
                    story.append(Paragraph(f"• {desc_text}", project_description_style))
                else:
                    # Fallback: treat as title if no bullet marker
                    title_text = clean_line.lstrip('-•').strip()
                    story.append(Paragraph(title_text, project_title_style))
            elif current_section in ['SKILLS', 'TECHNICAL SKILLS']:
                # Special handling for skills: bold labels, normal skill lists
                clean_line = line.strip()
                
                if '__SKILL_LABEL__' in clean_line:
                    # Extract skill label and list
                    # Format: __SKILL_LABEL__Label:__/SKILL_LABEL__ skills list
                    start_marker = '__SKILL_LABEL__'
                    end_marker = '__/SKILL_LABEL__'
                    start_idx = clean_line.find(start_marker)
                    end_idx = clean_line.find(end_marker)
                    
                    if start_idx != -1 and end_idx != -1:
                        skill_label = clean_line[start_idx + len(start_marker):end_idx].strip()
                        skill_list = clean_line[end_idx + len(end_marker):].strip()
                        # Format: bold label + normal skill list
                        formatted_text = f"<b>{skill_label}</b> {skill_list}"
                        story.append(Paragraph(formatted_text, normal_style))
                    else:
                        story.append(Paragraph(clean_line, normal_style))
                else:
                    story.append(Paragraph(clean_line, normal_style))
            elif line.strip().startswith('-') or line.strip().startswith('•'):
                clean_line = line.strip().lstrip('-•').strip()
                story.append(Paragraph(f"• {clean_line}", bullet_style))
            else:
                # Determine style based on section
                if current_section in ['PROFESSIONAL SUMMARY', 'SUMMARY']:
                    style = summary_style
                else:
                    style = normal_style
                story.append(Paragraph(line.strip(), style))
            i += 1

    @staticmethod
    def _generate_html(user, profile_data, template_name):
        """Generate professional HTML resume"""
        
        # First generate the enhanced resume text using templates
        class SimpleUser:
            def __init__(self, user_obj, profile_data):
                self.name = getattr(user_obj, 'name', profile_data.get('name', '[Your Name]'))
                self.email = getattr(user_obj, 'email', profile_data.get('email', '[Your Email]'))

        class SimpleProfile:
            def __init__(self, data, user_obj):
                self.headline = data.get('headline', '')
                self.phone = data.get('phone', '[Your Phone]')
                self.linkedin = data.get('linkedin', '')
                self.github = data.get('github', '')
                self.email = data.get('email', getattr(user_obj, 'email', '[Your Email]'))
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

        simple_user = SimpleUser(user, profile_data)
        simple_profile = SimpleProfile(profile_data, user)

        # Generate enhanced resume text
        resume_text = ResumeTemplates.generate_from_template(template_name, simple_user, simple_profile)
        
        # Get user data
        name = simple_user.name
        email = simple_user.email
        phone = simple_profile.phone
        linkedin = simple_profile.linkedin
        github = simple_profile.github
        leetcode = simple_profile.leetcode
        headline = simple_profile.headline
        
        # Build contact line
        contact_links = []
        
        def format_link(url):
            if not url.startswith("http"):
                return "https://" + url
            return url

        if linkedin:
            contact_links.append(
                f'<a href="{format_link(linkedin)}" target="_blank" class="profile-link">LinkedIn</a>'
            )

        if github:
            contact_links.append(
                f'<a href="{format_link(github)}" target="_blank" class="profile-link">GitHub</a>'
            )

        if leetcode:
            contact_links.append(
                f'<a href="{format_link(leetcode)}" target="_blank" class="profile-link">LeetCode</a>'
            )
        
        contact_line = ' | '.join(contact_links) if contact_links else ''
        
        # Parse the resume text for sections to display
        resume_lines = resume_text.split('\n')
        sections_html = ''
        current_section = None
        section_content = []
        
        for line in resume_lines:
            if '─' in line:
                # Skip separator lines
                continue
            elif line.isupper() and len(line) > 3:
                # New section
                if current_section and section_content:
                    # Special handling for projects section
                    if current_section == 'PROJECTS' or current_section == 'PROJECTS & ACHIEVEMENTS':
                        sections_html += f'<div class="section-title">{current_section}</div>\n'
                        for item in section_content:
                            item = item.strip()
                            if '__TITLE__' in item:
                                # Project title - display as bold without bullet
                                title_text = item.replace('__TITLE__', '').strip()
                                sections_html += f'  <div class="project-title"><strong>{title_text}</strong></div>\n'
                            elif item.startswith('•') or item.startswith('-'):
                                # Project description - display as bullet
                                clean = item.lstrip('-•').strip()
                                sections_html += f'  <div class="project-desc">• {clean}</div>\n'
                            else:
                                sections_html += f'  <div class="project-desc">{item}</div>\n'
                    elif current_section == 'PROFESSIONAL SUMMARY' or current_section == 'PROFESSIONAL HEADLINE':
                        content_html = '\n'.join(section_content)
                        sections_html += f'<p style="margin-bottom: 15px; text-align: justify; color: #555;">{content_html}</p>\n'
                    else:
                        sections_html += f'<div class="section-title">{current_section}</div>\n'
                        # Check if this is a skills section
                        is_skills_section = current_section.lower() in ['skills', 'technical skills']
                        
                        if is_skills_section:
                            # Skills are displayed as text lines, not list items
                            for item in section_content:
                                if '__SKILL_LABEL__' in item:
                                    # Extract and format skill label in bold
                                    # Format: __SKILL_LABEL__Label:__/SKILL_LABEL__ skills list
                                    start_marker = '__SKILL_LABEL__'
                                    end_marker = '__/SKILL_LABEL__'
                                    start_idx = item.find(start_marker)
                                    end_idx = item.find(end_marker)
                                    
                                    if start_idx != -1 and end_idx != -1:
                                        skill_label = item[start_idx + len(start_marker):end_idx].strip()
                                        skill_list = item[end_idx + len(end_marker):].strip()
                                        sections_html += f'<p><strong style="color: #000;">{skill_label}</strong> {skill_list}</p>\n'
                                    else:
                                        sections_html += f'<p>{item}</p>\n'
                                else:
                                    sections_html += f'<p>{item}</p>\n'
                        else:
                            # Regular sections with bullet points
                            sections_html += '<ul>\n'
                            for item in section_content:
                                if item.strip().startswith('-') or item.strip().startswith('•'):
                                    clean = item.strip().lstrip('-•').strip()
                                    sections_html += f'  <li>{clean}</li>\n'
                                else:
                                    sections_html += f'  <li>{item}</li>\n'
                            sections_html += '</ul>\n'
                
                current_section = line.strip()
                section_content = []
            elif current_section and line.strip():
                section_content.append(line.strip())
        
        # Add last section
        if current_section and section_content:
            # Special handling for projects section
            if current_section == 'PROJECTS' or current_section == 'PROJECTS & ACHIEVEMENTS':
                sections_html += f'<div class="section-title">{current_section}</div>\n'
                for item in section_content:
                    item = item.strip()
                    if '__TITLE__' in item:
                        # Project title - display as bold without bullet
                        title_text = item.replace('__TITLE__', '').strip()
                        sections_html += f'  <div class="project-title"><strong>{title_text}</strong></div>\n'
                    elif item.startswith('•') or item.startswith('-'):
                        # Project description - display as bullet
                        clean = item.lstrip('-•').strip()
                        sections_html += f'  <div class="project-desc">• {clean}</div>\n'
                    else:
                        sections_html += f'  <div class="project-desc">{item}</div>\n'
            elif current_section == 'PROFESSIONAL SUMMARY' or current_section == 'PROFESSIONAL HEADLINE':
                content_html = '\n'.join(section_content)
                sections_html += f'<p style="margin-bottom: 15px; text-align: justify; color: #555;">{content_html}</p>\n'
            else:
                sections_html += f'<div class="section-title">{current_section}</div>\n'
                # Check if this is a skills section
                is_skills_section = current_section.lower() in ['skills', 'technical skills']
                
                if is_skills_section:
                    # Skills are displayed as text lines, not list items
                    for item in section_content:
                        if '__SKILL_LABEL__' in item:
                            # Extract and format skill label in bold
                            # Format: __SKILL_LABEL__Label:__/SKILL_LABEL__ skills list
                            start_marker = '__SKILL_LABEL__'
                            end_marker = '__/SKILL_LABEL__'
                            start_idx = item.find(start_marker)
                            end_idx = item.find(end_marker)
                            
                            if start_idx != -1 and end_idx != -1:
                                skill_label = item[start_idx + len(start_marker):end_idx].strip()
                                skill_list = item[end_idx + len(end_marker):].strip()
                                sections_html += f'<p><strong style="color: #000;">{skill_label}</strong> {skill_list}</p>\n'
                            else:
                                sections_html += f'<p>{item}</p>\n'
                        else:
                            sections_html += f'<p>{item}</p>\n'
                else:
                    # Regular sections with bullet points
                    sections_html += '<ul>\n'
                    for item in section_content:
                        if item.strip().startswith('-') or item.strip().startswith('•'):
                            clean = item.strip().lstrip('-•').strip()
                            sections_html += f'  <li>{clean}</li>\n'
                        else:
                            sections_html += f'  <li>{item}</li>\n'
                    sections_html += '</ul>\n'
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Resume</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }}
        
        .container {{
            max-width: 900px;
            margin: 20px auto;
            padding: 40px;
            background-color: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #333;
            padding-bottom: 20px;
        }}
        
        .name {{
            font-size: 32px;
            font-weight: bold;
            color: #000;
            margin-bottom: 5px;
        }}
        
        .headline {{
            font-size: 16px;
            font-weight: bold;
            color: #000;
            margin-bottom: 15px;
        }}
        
        .contact {{
            font-size: 13px;
            color: #555;
            line-height: 1.8;
        }}
        
        .contact-item {{
            display: inline;
            margin-right: 15px;
        }}
        
        .profile-link {{
            font-weight: bold;
            color: #000;
            text-decoration: none;
        }}
        .profile-link:hover {{
            text-decoration: underline;
        }}
        
        .section-title {{
            font-size: 14px;
            font-weight: bold;
            text-transform: uppercase;
            color: #000;
            border-bottom: 2px solid #333;
            padding-bottom: 8px;
            margin-top: 25px;
            margin-bottom: 12px;
            letter-spacing: 0.5px;
        }}
        
        ul {{
            margin-left: 20px;
            margin-bottom: 15px;
        }}
        
        li {{
            margin-bottom: 8px;
            color: #555;
            line-height: 1.6;
        }}
        
        p {{
            margin-bottom: 10px;
        }}
        
        strong {{
            color: #000;
        }}
        
        .project-title {{
            font-weight: bold;
            font-size: 12px;
            margin-top: 10px;
            margin-bottom: 4px;
            color: #000;
        }}
        
        .project-desc {{
            margin-left: 20px;
            margin-bottom: 8px;
            color: #555;
            line-height: 1.6;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="name">{name}</div>
            {f'<div class="headline">{headline}</div>' if headline else ''}
            <div class="contact">
                {f'<span class="contact-item">📞 {phone}</span>' if phone and phone != '[Your Phone]' else ''}
                {f'<span class="contact-item">📧 <a href="mailto:{email}" style="color: #0066cc; text-decoration: none;">{email}</a></span>' if email else ''}
                {f'<span class="contact-item">{contact_line}</span>' if contact_line else ''}
            </div>
        </div>
        
        {sections_html}
    </div>
</body>
</html>"""
        
        return html_content.encode('utf-8'), 'text/html'

    @staticmethod
    def get_supported_formats():
        """Get list of supported export formats"""
        return [
            {'format': 'txt', 'name': 'Plain Text', 'extension': '.txt', 'content_type': 'text/plain'},
            {'format': 'html', 'name': 'HTML Document', 'extension': '.html', 'content_type': 'text/html'},
            {'format': 'pdf', 'name': 'PDF Document', 'extension': '.pdf', 'content_type': 'application/pdf'},
            {'format': 'docx', 'name': 'Word Document', 'extension': '.docx', 'content_type': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}
        ]