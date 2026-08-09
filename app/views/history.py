from datetime import datetime
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user_optional
from app.models.analysis import AnalysisHistory
from app.models.resume import Resume

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(tags=["History & Analysis Views"])

@router.get("/history", response_class=HTMLResponse)
def history_view(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_optional)
):
    if not current_user:
        return RedirectResponse(url="/login")

    analyses = db.query(AnalysisHistory).filter(AnalysisHistory.user_id == current_user.id).order_by(AnalysisHistory.created_at.desc()).all()
    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={"user": current_user, "analyses": analyses}
    )

@router.get("/analysis/demo", response_class=HTMLResponse)
def demo_analysis_view(
    request: Request,
    current_user = Depends(get_current_user_optional)
):
    # Mock analysis object with realistic values
    class MockAnalysis:
        def __init__(self):
            self.id = "demo"
            self.created_at = datetime.now()
            self.job_title = "Senior Software Engineer (Demo)"
            self.overall_score = 85.0
            self.ats_score = 82.0
            self.formatting_score = 90.0
            self.readability_score = 88.0
            self.skill_match_score = 80.0
            self.keyword_match_score = 84.0
            self.experience_score = 85.0
            self.education_score = 95.0
            self.project_score = 80.0
            self.matched_skills = ["Python", "FastAPI", "React", "Docker", "PostgreSQL", "Git"]
            self.missing_skills = ["AWS", "Redis", "Kubernetes"]
            self.recommended_skills = ["GraphQL", "CI/CD"]
            self.suggestions_json = {
                "formatting": ["Include contact links like LinkedIn and GitHub in a clear format.", "Avoid using complex column layouts that confuse older ATS parsers."],
                "readability": ["Add more high-impact action verbs at the beginning of bullet points.", "Quantify achievements under Acme Corp experience section."],
                "keywords": ["Incorporate 'AWS' or cloud deployment experience keywords.", "Include 'Redis' for caching context under projects section."]
            }

    class MockResume:
        def __init__(self):
            self.filename = "alex_morgan_resume.pdf"
            self.file_type = "pdf"
            self.file_size = 124530

    analysis = MockAnalysis()
    resume = MockResume()

    return templates.TemplateResponse(
        request=request,
        name="analysis_detail.html",
        context={
            "user": current_user,
            "analysis": analysis,
            "resume": resume
        }
    )

@router.get("/analysis/{analysis_id}", response_class=HTMLResponse)
def analysis_detail_view(
    analysis_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_optional)
):
    if not current_user:
        return RedirectResponse(url="/login")

    analysis = db.query(AnalysisHistory).filter(AnalysisHistory.id == analysis_id, AnalysisHistory.user_id == current_user.id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis record not found")

    resume = db.query(Resume).filter(Resume.id == analysis.resume_id).first()

    return templates.TemplateResponse(
        request=request,
        name="analysis_detail.html",
        context={
            "user": current_user,
            "analysis": analysis,
            "resume": resume
        }
    )
