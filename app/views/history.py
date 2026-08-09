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
