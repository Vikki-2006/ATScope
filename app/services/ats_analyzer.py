import re
from typing import Dict, Any, List

class ATSAnalyzer:
    @classmethod
    def analyze(cls, parsed_data: Dict[str, Any], job_match_data: Dict[str, Any] = None) -> Dict[str, Any]:
        text = parsed_data.get("raw_text", "")
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        word_count = len(text.split())
        
        # 1. Formatting Score (0 - 100)
        formatting_score = cls._calculate_formatting_score(text, lines, word_count, parsed_data)
        
        # 2. Readability Score (0 - 100)
        readability_score = cls._calculate_readability_score(text, word_count)
        
        # 3. Skill Match Score (0 - 100)
        skills = parsed_data.get("skills", [])
        skill_score = min(100.0, max(20.0, len(skills) * 8.0))
        
        # 4. Experience Score (0 - 100)
        exp_list = parsed_data.get("experience", [])
        experience_score = cls._calculate_experience_score(exp_list, text)
        
        # 5. Education Score (0 - 100)
        edu_list = parsed_data.get("education", [])
        education_score = 90.0 if edu_list else 50.0
        
        # 6. Project Score (0 - 100)
        projects = parsed_data.get("projects", [])
        project_score = min(100.0, max(40.0, len(projects) * 25.0))
        
        # 7. Keyword Match Score (0 - 100)
        if job_match_data and "keyword_match_score" in job_match_data:
            keyword_score = job_match_data["keyword_match_score"]
        else:
            keyword_score = min(100.0, max(30.0, len(skills) * 6.5 + (20.0 if "action verbs" in text.lower() else 10.0)))
            
        # 8. Overall ATS Score calculation
        weights = {
            "formatting": 0.15,
            "readability": 0.15,
            "skill": 0.25,
            "experience": 0.20,
            "education": 0.10,
            "project": 0.10,
            "keyword": 0.05
        }
        
        ats_score = (
            formatting_score * weights["formatting"] +
            readability_score * weights["readability"] +
            skill_score * weights["skill"] +
            experience_score * weights["experience"] +
            education_score * weights["education"] +
            project_score * weights["project"] +
            keyword_score * weights["keyword"]
        )
        
        overall_score = (ats_score * 0.6) + ((job_match_data.get("match_score", ats_score) if job_match_data else ats_score) * 0.4)
        
        return {
            "ats_score": round(ats_score, 1),
            "formatting_score": round(formatting_score, 1),
            "readability_score": round(readability_score, 1),
            "keyword_match_score": round(keyword_score, 1),
            "skill_match_score": round(skill_score, 1),
            "experience_score": round(experience_score, 1),
            "education_score": round(education_score, 1),
            "project_score": round(project_score, 1),
            "overall_score": round(overall_score, 1)
        }

    @staticmethod
    def _calculate_formatting_score(text: str, lines: List[str], word_count: int, parsed_data: Dict[str, Any]) -> float:
        score = 100.0
        # Penalize if too short or excessively long
        if word_count < 150:
            score -= 30.0
        elif word_count > 1200:
            score -= 15.0
            
        # Check contact details presence
        if not parsed_data.get("email"):
            score -= 15.0
        if not parsed_data.get("phone"):
            score -= 10.0
        if not parsed_data.get("linkedin"):
            score -= 5.0
            
        # Check standard sections
        if not parsed_data.get("skills"):
            score -= 15.0
        if not parsed_data.get("experience"):
            score -= 10.0
            
        # Check bullet point formatting usage
        bullet_count = sum(1 for line in lines if line.startswith(("-", "•", "*", "1.", "2.", "3.")))
        if bullet_count < 3:
            score -= 10.0
            
        return max(20.0, score)

    @staticmethod
    def _calculate_readability_score(text: str, word_count: int) -> float:
        if word_count == 0:
            return 0.0
        sentences = max(1, len(re.split(r'[.!?]+', text)))
        words_per_sentence = word_count / sentences
        
        # Optimal words per sentence in a resume is 12-20
        if 10 <= words_per_sentence <= 22:
            base_score = 92.0
        elif 8 <= words_per_sentence <= 28:
            base_score = 80.0
        else:
            base_score = 65.0
            
        # Check presence of measurable achievements/quantifiable metrics (% or $)
        metrics_count = len(re.findall(r'\b\d+%\b|\$\d+|\b\d+\s*(?:k|m|users|clients|projects|million|thousand)\b', text, re.IGNORECASE))

        metrics_bonus = min(10.0, metrics_count * 2.5)
        
        return min(100.0, base_score + metrics_bonus)

    @staticmethod
    def _calculate_experience_score(exp_list: List[Dict[str, Any]], text: str) -> float:
        if not exp_list:
            return 40.0
        score = 60.0 + min(30.0, len(exp_list) * 10.0)
        
        # Check for strong action verbs in experience
        action_verbs = ["developed", "built", "designed", "architected", "managed", "led", "optimized", "implemented", "scaled", "created", "spearheaded", "engineered"]
        found_verbs = sum(1 for verb in action_verbs if verb in text.lower())
        verb_bonus = min(10.0, found_verbs * 1.5)
        
        return min(100.0, score + verb_bonus)
