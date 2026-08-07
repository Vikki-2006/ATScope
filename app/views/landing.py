from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.deps import get_current_user_optional

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(tags=["Landing Page"])

@router.get("/", response_class=HTMLResponse)
def landing_page(request: Request, current_user = Depends(get_current_user_optional)):
    return templates.TemplateResponse(request=request, name="landing.html", context={"user": current_user})
