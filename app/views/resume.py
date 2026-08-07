from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user_optional
from app.models.resume import Resume

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(tags=["Resume Views"])

@router.get("/upload", response_class=HTMLResponse)
def upload_view(request: Request, current_user = Depends(get_current_user_optional)):
    if not current_user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse(request=request, name="upload.html", context={"user": current_user})

@router.get("/job-match", response_class=HTMLResponse)
def job_match_view(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_optional)
):
    if not current_user:
        return RedirectResponse(url="/login")
    
    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.created_at.desc()).all()
    return templates.TemplateResponse(
        request=request,
        name="job_match.html",
        context={"user": current_user, "resumes": resumes}
    )
