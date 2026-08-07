import re
from typing import Dict, Any, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.services.parser import COMMON_SKILLS

class JobMatcher:
    @classmethod
    def match(cls, resume_text: str, resume_skills: List[str], job_description: str) -> Dict[str, Any]:
        if not job_description or not job_description.strip():
            return {
                "match_score": 0.0,
                "keyword_match_score": 0.0,
                "matched_skills": [],
                "missing_skills": [],
                "recommended_skills": [],
                "missing_keywords": []
            }
            
        # 1. Cosine similarity score via TF-IDF
        cosine_sim = cls._calculate_cosine_similarity(resume_text, job_description)
        
        # 2. Extract skills from Job Description
        jd_skills = cls._extract_jd_skills(job_description)
        
        # 3. Match Skills against Resume Skills
        resume_skills_lower = {s.lower() for s in resume_skills}
        
        matched_skills_set = set()
        missing_skills_set = set()
        
        for skill in jd_skills:
            if skill.lower() in resume_skills_lower or any(skill.lower() in rs for rs in resume_skills_lower):
                matched_skills_set.add(skill)
            else:
                missing_skills_set.add(skill)
                
        matched_skills = sorted(list(matched_skills_set))
        missing_skills = sorted(list(missing_skills_set))
        
        # 4. Calculate skill match score
        total_jd_skills = len(jd_skills)
        if total_jd_skills > 0:
            skill_match_ratio = (len(matched_skills) / total_jd_skills) * 100.0
        else:
            skill_match_ratio = 70.0
            
        # 5. Extract Missing Keywords (frequent nouns/tech terms in JD not in resume)
        missing_keywords = cls._extract_missing_keywords(resume_text, job_description)
        
        # 6. Overall Job Match Score (combined cosine similarity + skill match)
        overall_match = (cosine_sim * 0.4) + (skill_match_ratio * 0.6)
        overall_match = min(98.0, max(15.0, round(overall_match, 1)))
        
        # Recommended Skills (high priority missing skills + industry standards)
        recommended_skills = missing_skills[:6]
        if len(recommended_skills) < 4:
            # Supplement with popular related skills
            popular = ["Docker", "AWS", "CI/CD", "Redis", "Unit Testing", "System Design"]
            for p in popular:
                if p not in matched_skills and p not in recommended_skills:
                    recommended_skills.append(p)
                if len(recommended_skills) >= 6:
                    break
                    
        return {
            "match_score": overall_match,
            "keyword_match_score": round(skill_match_ratio, 1),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "recommended_skills": recommended_skills,
            "missing_keywords": missing_keywords
        }

    @staticmethod
    def _calculate_cosine_similarity(text1: str, text2: str) -> float:
        try:
            vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(sim * 100.0)
        except Exception:
            return 50.0

    @staticmethod
    def _extract_jd_skills(job_description: str) -> List[str]:
        found = set()
        jd_lower = job_description.lower()
        for skill in COMMON_SKILLS:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, jd_lower):
                found.add(skill.title() if len(skill) > 3 else skill.upper())
        return sorted(list(found))

    @staticmethod
    def _extract_missing_keywords(resume_text: str, job_description: str) -> List[str]:
        resume_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', resume_text.lower()))
        jd_words = re.findall(r'\b[a-zA-Z]{4,}\b', job_description.lower())
        
        # Stop words to exclude
        stopwords = {
            "with", "that", "this", "from", "they", "will", "have", "more", "about",
            "their", "which", "would", "there", "work", "team", "experience", "role",
            "position", "company", "looking", "candidate", "ability", "must", "should",
            "using", "years", "working", "strong", "knowledge", "skills", "good"
        }
        
        word_freq = {}
        for w in jd_words:
            if w not in stopwords and w not in resume_words:
                word_freq[w] = word_freq.get(w, 0) + 1
                
        sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [kw[0].title() for kw in sorted_keywords[:8]]
