"""
AI Resume Optimization Service
Analyzes resume against job descriptions using NLP techniques
"""
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from groq import Groq
from backend.config import Config

class ResumeOptimizer:
    """Resume optimization using TF-IDF and Cosine Similarity"""
    
    # Common stop words to exclude from keywords
    STOP_WORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'for', 'to',
        'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these',
        'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which',
        'who', 'when', 'where', 'why', 'how', 'as', 'if', 'because', 'so',
        'than', 'such', 'no', 'not', 'only', 'own', 'same', 'so', 'some',
        'other', 'more', 'most', 'very', 'just', 'my', 'your', 'his', 'her'
    }
    
    @staticmethod
    def clean_text(text):
        """Clean and normalize text"""
        if not text:
            return ""
        # Convert to lowercase
        text = text.lower()
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-z0-9\s\-+#]', ' ', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    @staticmethod
    def extract_keywords(text, num_keywords=15):
        """Extract important keywords from text using word frequency"""
        cleaned = ResumeOptimizer.clean_text(text)
        words = cleaned.split()
        
        # Filter out stop words and short words
        keywords = [
            word for word in words 
            if word not in ResumeOptimizer.STOP_WORDS 
            and len(word) > 2
            and not word.isdigit()
        ]
        
        # Count frequency
        from collections import Counter
        freq = Counter(keywords)
        
        # Get top keywords
        top_keywords = [word for word, _ in freq.most_common(num_keywords)]
        return top_keywords
    
    @staticmethod
    def calculate_match_score(resume_text, job_description_text):
        """
        Calculate match score between resume and job description
        
        Args:
            resume_text: User's resume content
            job_description_text: Job description to match
            
        Returns:
            Dictionary containing:
            - match_score: Percentage match (0-100)
            - missing_keywords: Skills in JD but not in resume
            - overlapping_keywords: Skills in both
            - suggestions: Improvement recommendations
        """
        if not resume_text or not job_description_text:
            return {
                'match_score': 0,
                'missing_keywords': [],
                'overlapping_keywords': [],
                'suggestions': ['Please provide both resume and job description']
            }
        
        # Clean texts
        resume_clean = ResumeOptimizer.clean_text(resume_text)
        jd_clean = ResumeOptimizer.clean_text(job_description_text)
        
        # Extract keywords
        resume_keywords = set(ResumeOptimizer.extract_keywords(resume_clean, 20))
        jd_keywords = set(ResumeOptimizer.extract_keywords(jd_clean, 25))
        
        # Calculate overlapping and missing keywords
        overlapping = resume_keywords.intersection(jd_keywords)
        missing = jd_keywords - resume_keywords
        
        # TF-IDF and Cosine Similarity calculation
        vectorizer = TfidfVectorizer(
            max_features=100,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        try:
            tfidf_matrix = vectorizer.fit_transform([resume_clean, jd_clean])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            match_score_base = int(similarity * 100)
        except:
            match_score_base = 0
        
        # Boost score based on keyword overlap (40% base similarity, 60% keyword overlap)
        keyword_overlap_ratio = len(overlapping) / len(jd_keywords) if jd_keywords else 0
        keyword_score = int(keyword_overlap_ratio * 100)
        
        # Weighted match score
        match_score = int(0.4 * match_score_base + 0.6 * keyword_score)
        match_score = min(100, max(0, match_score))
        
        # Generate suggestions
        suggestions = ResumeOptimizer.generate_suggestions(
            missing, 
            overlapping, 
            resume_clean,
            jd_clean
        )
        
        return {
            'match_score': match_score,
            'missing_keywords': sorted(list(missing))[:10],  # Top 10 missing
            'overlapping_keywords': sorted(list(overlapping))[:10],  # Top 10 overlapping
            'suggestions': suggestions
        }
    
    @staticmethod
    def generate_suggestions(missing_keywords, found_keywords, resume_text, jd_text):
        """Generate actionable improvement suggestions"""
        suggestions = []
        
        # Suggestion 1: Add missing technical skills
        if missing_keywords:
            top_missing = sorted(list(missing_keywords))[:5]
            if top_missing:
                keywords_str = ', '.join(top_missing)
                suggestions.append(
                    f"Add experience or mention these key skills: {keywords_str}"
                )
        
        # Suggestion 2: Emphasize matching skills
        if found_keywords:
            top_found = sorted(list(found_keywords))[:5]
            if top_found:
                keywords_str = ', '.join(top_found)
                suggestions.append(
                    f"Highlight your expertise in: {keywords_str}"
                )
        
        # Suggestion 3: Keyword density
        if len(missing_keywords) > len(found_keywords):
            suggestions.append(
                "Increase coverage of job description requirements. "
                f"You're missing {len(missing_keywords)} key terms."
            )
        
        # Suggestion 4: Leverage industry terminology
        if missing_keywords:
            missing_list = sorted(list(missing_keywords))[:3]
            if missing_list:
                suggestions.append(
                    f"Incorporate industry-specific terms like: {', '.join(missing_list)} "
                    "in your work experience descriptions"
                )
        
        # Suggestion 5: Match job benefits
        if len(found_keywords) / (len(found_keywords) + len(missing_keywords) + 0.1) < 0.5:
            suggestions.append(
                "Your resume covers less than 50% of job requirements. "
                "Consider adding more relevant experience or certifications."
            )
        else:
            suggestions.append(
                f"Great! Your resume matches {int((len(found_keywords) / (len(found_keywords) + len(missing_keywords) + 0.1)) * 100)}% "
                "of the job requirements."
            )
        
        # AI-enhanced suggestion
        ai_suggestion = ResumeOptimizer.generate_ai_suggestion(resume_text, jd_text, missing_keywords, found_keywords)
        if ai_suggestion:
            suggestions.append(ai_suggestion)
        
        return suggestions[:5]  # Return top 5 suggestions
    
    @staticmethod
    def generate_ai_suggestion(resume_text, jd_text, missing_keywords, found_keywords):
        """Generate AI-powered suggestion using Groq"""
        try:
            client = Groq(api_key=Config.GROQ_API_KEY)
            
            prompt = f"""
            Based on this job description and resume, provide one specific, actionable suggestion to improve the resume's match.

            Job Description:
            {jd_text[:500]}...

            Resume:
            {resume_text[:500]}...

            Missing keywords: {', '.join(list(missing_keywords)[:5])}
            Found keywords: {', '.join(list(found_keywords)[:5])}

            Give a concise, professional suggestion (1-2 sentences) on how to improve the resume.
            """
            
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"AI suggestion generation failed: {e}")
            return None
