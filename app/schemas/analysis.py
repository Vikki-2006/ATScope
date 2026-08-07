from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class AnalysisRequest(BaseModel):
    resume_id: int
    job_title: Optional[str] = None
    job_description: Optional[str] = None

class AnalysisResponse(BaseModel):
    id: int
    user_id: int
    resume_id: int
    job_title: Optional[str] = None
    job_description: Optional[str] = None
    
    ats_score: float
    formatting_score: float
    readability_score: float
    keyword_match_score: float
    skill_match_score: float
    experience_score: float
    education_score: float
    project_score: float
    overall_score: float
    
    matched_skills: Optional[List[str]] = []
    missing_skills: Optional[List[str]] = []
    recommended_skills: Optional[List[str]] = []
    missing_keywords: Optional[List[str]] = []
    suggestions_json: Optional[Dict[str, List[str]]] = None
    
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
