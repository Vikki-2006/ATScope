from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class ResumeParsedData(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    skills: List[str] = []
    education: List[Dict[str, Any]] = []
    experience: List[Dict[str, Any]] = []
    projects: List[Dict[str, Any]] = []
    certifications: List[str] = []
    languages: List[str] = []
    summary: Optional[str] = None

class ResumeCreate(BaseModel):
    filename: str
    file_type: str
    file_size: int

class ResumeResponse(BaseModel):
    id: int
    user_id: int
    filename: str
    file_path: str
    file_type: str
    file_size: int
    raw_text: str
    parsed_data: Optional[Dict[str, Any]] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
