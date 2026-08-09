import os
from pathlib import Path
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

IS_VERCEL: bool = bool(os.getenv("VERCEL"))

if IS_VERCEL:
    UPLOAD_DIR = Path("/tmp/atscope_uploads")
else:
    UPLOAD_DIR = BASE_DIR / "app" / "static" / "uploads"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Resume Analyzer"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = "super-secret-key-change-this-in-production-resume-analyzer-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    DATABASE_URL: str = ""
    
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: set[str] = {"pdf", "docx"}
    
    model_config = ConfigDict(case_sensitive=True)

    def model_post_init(self, __context):
        if IS_VERCEL and not self.DATABASE_URL:
            raise RuntimeError(
                "DATABASE_URL environment variable is missing on Vercel deployment. "
                "Please configure DATABASE_URL in Vercel Project Settings -> Environment Variables."
            )
        if not self.DATABASE_URL:
            self.DATABASE_URL = f"sqlite:///{BASE_DIR}/resume_analyzer.db"
            
        if self.DATABASE_URL.startswith("postgres://"):
            self.DATABASE_URL = self.DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
        elif self.DATABASE_URL.startswith("postgresql://") and not self.DATABASE_URL.startswith("postgresql+psycopg://"):
            self.DATABASE_URL = self.DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

settings = Settings()

