"""
AI-powered content compression for fitting resume to single page
"""


class AIContentCompressor:
    """Service for compressing resume content intelligently while maintaining quality"""

    @staticmethod
    def compress_summary(summary):
        """
        Compress professional summary to maximum 3 lines while preserving key information
        """
        if not summary:
            return summary
        
        lines = summary.strip().split('\n')
        
        # If already 3 lines or less, return as is
        if len(lines) <= 3:
            return summary
        
        # Strategy 1: Keep first 3 lines if they're complete
        compressed = '\n'.join(lines[:3])
        
        # Strategy 2: If summary is very long, aim for 2 lines
        words = summary.split()
        if len(words) > 60:
            # Take roughly first 40-50 words, break at sentence boundary
            result = ''
            word_count = 0
            for word in words:
                result += word + ' '
                word_count += 1
                if word_count >= 40 and word.endswith(('.', '!', '?')):
                    break
            compressed = result.strip()
        
        return compressed

    @staticmethod
    def compress_projects(projects):
        """
        Limit projects to 2 bullet points per project, max 4 projects
        """
        if not projects:
            return projects
        
        if isinstance(projects, str):
            # Parse project structure from text
            lines = projects.split('\n')
            compressed_lines = []
            project_count = 0
            bullet_count = 0
            
            for line in lines:
                # Check if it's a project header (typically bold or no bullet)
                if line.strip() and not line.strip().startswith('-') and not line.strip().startswith('•'):
                    if project_count > 0:
                        bullet_count = 0
                    if project_count < 4:
                        compressed_lines.append(line)
                        project_count += 1
                # Check if it's a bullet point
                elif line.strip().startswith('-') or line.strip().startswith('•'):
                    if project_count > 0 and bullet_count < 2:
                        compressed_lines.append(line)
                        bullet_count += 1
            
            return '\n'.join(compressed_lines)
        
        return projects

    @staticmethod
    def compress_skills(skills):
        """
        Merge skill lines to reduce vertical space
        """
        if not skills:
            return skills
        
        if isinstance(skills, str):
            lines = [line.strip() for line in skills.split('\n') if line.strip()]
            
            # If skills span multiple lines, try to condense
            if len(lines) > 3:
                # Group skills by category (assuming format like "Category: skill1, skill2")
                condensed = []
                for line in lines:
                    if ':' in line:
                        # Keep skill categories
                        condensed.append(line)
                    else:
                        # Try to append to previous line if possible
                        if condensed and len(condensed[-1]) < 80:
                            condensed[-1] += ', ' + line
                        else:
                            condensed.append(line)
                
                return '\n'.join(condensed[:3])  # Limit to 3 lines
            
            return skills
        
        return skills

    @staticmethod
    def compress_experience(experience):
        """
        Limit experience entries to 2 bullet points each
        """
        return AIContentCompressor.compress_projects(experience)
