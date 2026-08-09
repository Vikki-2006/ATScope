import os
from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1 import api_router

from app.views.landing import router as landing_views
from app.views.auth import router as auth_views
from app.views.dashboard import router as dashboard_views
from app.views.resume import router as resume_views
from app.views.history import router as history_views
from app.views.settings import router as settings_views

# Initialize Database Tables (Local development fallback)
if not os.getenv("VERCEL"):
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static Files Mount
static_dir = os.path.join(os.path.dirname(__file__), "app", "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include HTML View Routers
app.include_router(landing_views)
app.include_router(auth_views)
app.include_router(dashboard_views)
app.include_router(resume_views)
app.include_router(history_views)
app.include_router(settings_views)

# Include REST API Router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Global 404 Handler
templates = Jinja2Templates(directory="app/templates")

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    if request.url.path.startswith("/api/"):
        return JSONResponse(status_code=404, content={"detail": "API Endpoint Not Found"})
    return templates.TemplateResponse(request=request, name="landing.html", context={"user": None}, status_code=404)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
