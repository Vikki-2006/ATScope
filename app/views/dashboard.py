from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user_optional
from app.models.resume import Resume
from app.models.analysis import AnalysisHistory

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(tags=["Dashboard View"])

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_view(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_optional)
):
    if not current_user:
        return RedirectResponse(url="/login")

    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.created_at.desc()).all()
    recent_analyses = db.query(AnalysisHistory).filter(AnalysisHistory.user_id == current_user.id).order_by(AnalysisHistory.created_at.desc()).limit(5).all()
    
    total_resumes = len(resumes)
    total_analyses = db.query(AnalysisHistory).filter(AnalysisHistory.user_id == current_user.id).count()

    if recent_analyses:
        avg_ats = round(sum(a.ats_score for a in recent_analyses) / len(recent_analyses), 1)
        avg_overall = round(sum(a.overall_score for a in recent_analyses) / len(recent_analyses), 1)
        avg_formatting = round(sum(a.formatting_score for a in recent_analyses) / len(recent_analyses), 1)
        avg_keyword = round(sum(a.keyword_match_score for a in recent_analyses) / len(recent_analyses), 1)
    else:
        avg_ats = 0.0
        avg_overall = 0.0
        avg_formatting = 0.0
        avg_keyword = 0.0

    stats = {
        "total_resumes": total_resumes,
        "total_analyses": total_analyses,
        "avg_ats": avg_ats,
        "avg_overall": avg_overall,
        "avg_formatting": avg_formatting,
        "avg_keyword": avg_keyword
    }

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "user": current_user,
            "resumes": resumes,
            "recent_analyses": recent_analyses,
            "stats": stats
        }
    )
