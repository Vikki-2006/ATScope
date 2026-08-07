from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.core.deps import get_current_user_optional, get_current_user

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(tags=["Auth Views"])

@router.get("/login", response_class=HTMLResponse)
def login_view(request: Request, current_user = Depends(get_current_user_optional)):
    if current_user:
        return RedirectResponse(url="/dashboard")
    return templates.TemplateResponse(request=request, name="auth/login.html", context={"user": None})

@router.get("/register", response_class=HTMLResponse)
def register_view(request: Request, current_user = Depends(get_current_user_optional)):
    if current_user:
        return RedirectResponse(url="/dashboard")
    return templates.TemplateResponse(request=request, name="auth/register.html", context={"user": None})

@router.get("/forgot-password", response_class=HTMLResponse)
def forgot_password_view(request: Request):
    return templates.TemplateResponse(request=request, name="auth/forgot_password.html", context={"user": None})

@router.get("/profile", response_class=HTMLResponse)
def profile_view(request: Request, current_user = Depends(get_current_user)):
    return templates.TemplateResponse(request=request, name="auth/profile.html", context={"user": current_user})
