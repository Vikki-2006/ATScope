import os
from pathlib import Path
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "app" / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Resume Analyzer"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-change-this-in-production-resume-analyzer-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/resume_analyzer.db")
    
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: set[str] = {"pdf", "docx"}
    
    model_config = ConfigDict(case_sensitive=True)

settings = Settings()
