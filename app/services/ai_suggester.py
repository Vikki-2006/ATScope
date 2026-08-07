from typing import Dict, Any, List

class AISuggester:
    @classmethod
    def generate_suggestions(
        cls, 
        parsed_data: Dict[str, Any], 
        ats_scores: Dict[str, Any], 
        job_match_data: Dict[str, Any] = None
    ) -> Dict[str, List[str]]:
        text = parsed_data.get("raw_text", "")
        skills = parsed_data.get("skills", [])
        experience = parsed_data.get("experience", [])
        projects = parsed_data.get("projects", [])
        summary = parsed_data.get("summary", "")
        
        missing_skills = job_match_data.get("missing_skills", []) if job_match_data else []
        missing_keywords = job_match_data.get("missing_keywords", []) if job_match_data else []
        
        suggestions = {
            "improve_summary": [],
            "rewrite_experience": [],
            "improve_bullet_points": [],
            "add_missing_skills": [],
            "improve_projects": [],
            "improve_formatting": [],
            "highlight_achievements": []
        }
        
        # 1. Summary Suggestions
        if not summary or len(summary.split()) < 20:
            suggestions["improve_summary"].append(
                "Add a strong 3-4 sentence Professional Summary at the top of your resume highlighting your key expertise, years of experience, and main technical domain."
            )
            suggestions["improve_summary"].append(
                "Include target job title keywords in your summary (e.g., 'Senior Full-Stack Engineer with 4+ years of expertise in Python & Cloud Architecture')."
            )
        else:
            suggestions["improve_summary"].append(
                "Enhance your summary by incorporating high-impact metrics (e.g., 'increased system throughput by 35%')."
            )
            
        # 2. Experience Rewrites
        if not experience:
            suggestions["rewrite_experience"].append(
                "No formal experience section detected. Format your work history clearly with Job Title, Company Name, Location, and Employment Dates."
            )
        else:
            suggestions["rewrite_experience"].append(
                "Begin every experience bullet point with strong action verbs (e.g., 'Architected', 'Spearheaded', 'Optimized', 'Automated')."
            )
            suggestions["rewrite_experience"].append(
                "Use the XYZ formula: 'Accomplished [X] as measured by [Y], by doing [Z]' for all bullet points."
            )
            
        # 3. Bullet Point Improvements
        suggestions["improve_bullet_points"].append(
            "Replace passive wording like 'was responsible for' or 'helped with' with direct action verbs like 'Engineered', 'Deployed', or 'Managed'."
        )
        suggestions["improve_bullet_points"].append(
            "Ensure bullet points are between 1 and 2 lines long for maximum readability."
        )
        
        # 4. Add Missing Skills
        if missing_skills:
            skills_str = ", ".join(missing_skills[:5])
            suggestions["add_missing_skills"].append(
                f"Incorporate key target skills required for this job: {skills_str}."
            )
        if len(skills) < 8:
            suggestions["add_missing_skills"].append(
                "Expand your skills section into categorized subsections: Technical Skills, Frameworks & Libraries, Databases, and DevOps Tools."
            )
            
        # 5. Project Improvements
        if not projects:
            suggestions["improve_projects"].append(
                "Add 2-3 technical projects with direct links to GitHub repositories or live demo URLs to demonstrate hands-on experience."
            )
        else:
            suggestions["improve_projects"].append(
                "For each project, explicitly state the technologies used, overall architecture, and quantifiable outcomes."
            )
            
        # 6. Formatting Improvements
        if ats_scores.get("formatting_score", 100) < 85:
            suggestions["improve_formatting"].append(
                "Use standard ATS section headings like 'Work Experience', 'Education', 'Skills', and 'Projects' instead of custom titles."
            )
            suggestions["improve_formatting"].append(
                "Ensure clean layout structure without embedded complex graphic tables, text boxes, or images which disrupt ATS parser indexing."
            )
            
        # 7. Highlight Achievements
        suggestions["highlight_achievements"].append(
            "Add quantifiable business metrics (e.g., '% reduction in latency', '$ saved', 'number of active users served')."
        )
        suggestions["highlight_achievements"].append(
            "Include key awards, recognitions, or certifications earned to stand out from other candidates."
        )

        return suggestions
