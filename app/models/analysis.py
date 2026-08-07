import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class AnalysisHistory(Base):
    __tablename__ = "analysis_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)
    job_title = Column(String(255), nullable=True)
    job_description = Column(Text, nullable=True)
    
    # Detailed Scores (0-100)
    ats_score = Column(Float, nullable=False, default=0.0)
    formatting_score = Column(Float, nullable=False, default=0.0)
    readability_score = Column(Float, nullable=False, default=0.0)
    keyword_match_score = Column(Float, nullable=False, default=0.0)
    skill_match_score = Column(Float, nullable=False, default=0.0)
    experience_score = Column(Float, nullable=False, default=0.0)
    education_score = Column(Float, nullable=False, default=0.0)
    project_score = Column(Float, nullable=False, default=0.0)
    overall_score = Column(Float, nullable=False, default=0.0)
    
    # Structured breakdown metrics & recommendations (JSON)
    matched_skills = Column(JSON, nullable=True)
    missing_skills = Column(JSON, nullable=True)
    recommended_skills = Column(JSON, nullable=True)
    missing_keywords = Column(JSON, nullable=True)
    suggestions_json = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="analyses")
    resume = relationship("Resume", back_populates="analyses")
