from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.resumes import router as resumes_router
from app.api.v1.analysis import router as analysis_router
from app.api.v1.user import router as user_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(resumes_router)
api_router.include_router(analysis_router)
api_router.include_router(user_router)
