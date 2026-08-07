from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user_optional
from app.models.user import UserSettings

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(tags=["Settings View"])

@router.get("/settings", response_class=HTMLResponse)
def settings_view(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_optional)
):
    if not current_user:
        return RedirectResponse(url="/login")

    user_settings = db.query(UserSettings).filter(UserSettings.user_id == current_user.id).first()
    if not user_settings:
        user_settings = UserSettings(user_id=current_user.id, theme="dark")
        db.add(user_settings)
        db.commit()
        db.refresh(user_settings)

    return templates.TemplateResponse(
        request=request,
        name="settings.html",
        context={
            "user": current_user,
            "settings": user_settings
        }
    )
