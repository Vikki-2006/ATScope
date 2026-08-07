import os
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings, UPLOAD_DIR
from app.core.deps import get_current_user
from app.models.user import User
from app.models.resume import Resume
from app.schemas.resume import ResumeResponse
from app.services.parser import ResumeParser

router = APIRouter(prefix="/resumes", tags=["Resumes"])

@router.post("/upload", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="File name is missing")

    filename = file.filename
    ext = filename.split(".")[-1].lower() if "." in filename else ""
    
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file format. Only {', '.join(settings.ALLOWED_EXTENSIONS).upper()} files are permitted."
        )

    # File size validation
    contents = await file.read()
    file_size = len(contents)
    if file_size > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=400, 
            detail=f"File size exceeds maximum limit of {settings.MAX_FILE_SIZE_MB}MB"
        )

    # Save to upload directory with unique filename
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    with open(file_path, "wb") as f:
        f.write(contents)

    # Parse resume text & extracted attributes
    parsed = ResumeParser.parse_file(file_path, ext)
    raw_text = parsed.get("raw_text", "")

    new_resume = Resume(
        user_id=current_user.id,
        filename=filename,
        file_path=file_path,
        file_type=ext,
        file_size=file_size,
        raw_text=raw_text,
        parsed_data=parsed
    )
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return new_resume

@router.get("", response_model=List[ResumeResponse])
def get_user_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.created_at.desc()).all()

@router.get("/{resume_id}", response_model=ResumeResponse)
def get_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume record not found")
    return resume

@router.delete("/{resume_id}", status_code=status.HTTP_200_OK)
def delete_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume record not found")
    
    if os.path.exists(resume.file_path):
        try:
            os.remove(resume.file_path)
        except Exception:
            pass

    db.delete(resume)
    db.commit()
    return {"message": "Resume successfully deleted"}
