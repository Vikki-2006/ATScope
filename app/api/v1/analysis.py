from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import StreamingResponse, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.resume import Resume
from app.models.analysis import AnalysisHistory
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
from app.services.ats_analyzer import ATSAnalyzer
from app.services.job_matcher import JobMatcher
from app.services.ai_suggester import AISuggester
from app.services.report_generator import ReportGenerator

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.post("/run", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
def run_analysis(
    request: AnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resume = db.query(Resume).filter(Resume.id == request.resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Selected resume was not found")

    parsed_data = resume.parsed_data or {}
    raw_text = resume.raw_text or ""
    resume_skills = parsed_data.get("skills", [])

    # Run Job Description matching if provided
    job_match_data = None
    if request.job_description and request.job_description.strip():
        job_match_data = JobMatcher.match(raw_text, resume_skills, request.job_description)

    # Run ATS analysis
    ats_scores = ATSAnalyzer.analyze(parsed_data, job_match_data)

    # Generate AI Suggestions
    suggestions = AISuggester.generate_suggestions(parsed_data, ats_scores, job_match_data)

    # Save to AnalysisHistory
    analysis = AnalysisHistory(
        user_id=current_user.id,
        resume_id=resume.id,
        job_title=request.job_title or "General Software Role",
        job_description=request.job_description,
        ats_score=ats_scores["ats_score"],
        formatting_score=ats_scores["formatting_score"],
        readability_score=ats_scores["readability_score"],
        keyword_match_score=ats_scores["keyword_match_score"],
        skill_match_score=ats_scores["skill_match_score"],
        experience_score=ats_scores["experience_score"],
        education_score=ats_scores["education_score"],
        project_score=ats_scores["project_score"],
        overall_score=ats_scores["overall_score"],
        matched_skills=job_match_data.get("matched_skills", []) if job_match_data else resume_skills[:10],
        missing_skills=job_match_data.get("missing_skills", []) if job_match_data else [],
        recommended_skills=job_match_data.get("recommended_skills", []) if job_match_data else ["Docker", "AWS", "CI/CD"],
        missing_keywords=job_match_data.get("missing_keywords", []) if job_match_data else [],
        suggestions_json=suggestions
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return analysis

@router.get("/history", response_model=List[AnalysisResponse])
def get_analysis_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(AnalysisHistory).filter(AnalysisHistory.user_id == current_user.id).order_by(AnalysisHistory.created_at.desc()).all()

@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis_detail(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    analysis = db.query(AnalysisHistory).filter(AnalysisHistory.id == analysis_id, AnalysisHistory.user_id == current_user.id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis record not found")
    return analysis

@router.get("/demo/report/pdf")
def download_demo_pdf_report():
    analysis_dict = {
        "job_title": "Senior Software Engineer (Demo)",
        "overall_score": 85.0,
        "ats_score": 82.0,
        "formatting_score": 90.0,
        "readability_score": 88.0,
        "keyword_match_score": 84.0,
        "skill_match_score": 80.0,
        "experience_score": 85.0,
        "education_score": 95.0,
        "project_score": 80.0,
        "matched_skills": ["Python", "FastAPI", "React", "Docker", "PostgreSQL", "Git"],
        "missing_skills": ["AWS", "Redis", "Kubernetes"],
        "recommended_skills": ["GraphQL", "CI/CD"],
        "suggestions_json": {
            "formatting": ["Include contact links like LinkedIn and GitHub in a clear format.", "Avoid using complex column layouts that confuse older ATS parsers."],
            "readability": ["Add more high-impact action verbs at the beginning of bullet points.", "Quantify achievements under Acme Corp experience section."],
            "keywords": ["Incorporate 'AWS' or cloud deployment experience keywords.", "Include 'Redis' for caching context under projects section."]
        }
    }
    pdf_bytes = ReportGenerator.generate_pdf_report(analysis_dict, "Demo Candidate")
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=Demo_Resume_Analysis_Report.pdf"}
    )

@router.get("/demo/report/csv")
def download_demo_csv_report():
    analysis_dict = {
        "job_title": "Senior Software Engineer (Demo)",
        "overall_score": 85.0,
        "ats_score": 82.0,
        "formatting_score": 90.0,
        "readability_score": 88.0,
        "keyword_match_score": 84.0,
        "skill_match_score": 80.0,
        "experience_score": 85.0,
        "education_score": 95.0,
        "project_score": 80.0,
        "matched_skills": ["Python", "FastAPI", "React", "Docker", "PostgreSQL", "Git"],
        "missing_skills": ["AWS", "Redis", "Kubernetes"],
        "recommended_skills": ["GraphQL", "CI/CD"]
    }
    csv_data = ReportGenerator.generate_csv_report(analysis_dict, "Demo Candidate")
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=Demo_Resume_Analysis_Report.csv"}
    )

@router.get("/{analysis_id}/report/pdf")
def download_pdf_report(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    analysis = db.query(AnalysisHistory).filter(AnalysisHistory.id == analysis_id, AnalysisHistory.user_id == current_user.id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis record not found")

    analysis_dict = {
        "job_title": analysis.job_title,
        "overall_score": analysis.overall_score,
        "ats_score": analysis.ats_score,
        "formatting_score": analysis.formatting_score,
        "readability_score": analysis.readability_score,
        "keyword_match_score": analysis.keyword_match_score,
        "skill_match_score": analysis.skill_match_score,
        "experience_score": analysis.experience_score,
        "education_score": analysis.education_score,
        "project_score": analysis.project_score,
        "matched_skills": analysis.matched_skills or [],
        "missing_skills": analysis.missing_skills or [],
        "recommended_skills": analysis.recommended_skills or [],
        "suggestions_json": analysis.suggestions_json or {}
    }

    pdf_bytes = ReportGenerator.generate_pdf_report(analysis_dict, current_user.full_name)
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=Resume_Analysis_Report_{analysis_id}.pdf"}
    )

@router.get("/{analysis_id}/report/csv")
def download_csv_report(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    analysis = db.query(AnalysisHistory).filter(AnalysisHistory.id == analysis_id, AnalysisHistory.user_id == current_user.id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis record not found")

    analysis_dict = {
        "job_title": analysis.job_title,
        "overall_score": analysis.overall_score,
        "ats_score": analysis.ats_score,
        "formatting_score": analysis.formatting_score,
        "readability_score": analysis.readability_score,
        "keyword_match_score": analysis.keyword_match_score,
        "skill_match_score": analysis.skill_match_score,
        "experience_score": analysis.experience_score,
        "education_score": analysis.education_score,
        "project_score": analysis.project_score,
        "matched_skills": analysis.matched_skills or [],
        "missing_skills": analysis.missing_skills or [],
        "recommended_skills": analysis.recommended_skills or []
    }

    csv_data = ReportGenerator.generate_csv_report(analysis_dict, current_user.full_name)
    
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=Resume_Analysis_Report_{analysis_id}.csv"}
    )
