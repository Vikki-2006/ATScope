from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.security import verify_password, hash_password
from app.models.user import User, UserSettings
from app.schemas.user import UserSettingsUpdate, PasswordChange, UserResponse

router = APIRouter(prefix="/user", tags=["User Settings"])

@router.put("/settings")
def update_user_settings(
    settings_in: UserSettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_settings = db.query(UserSettings).filter(UserSettings.user_id == current_user.id).first()
    if not user_settings:
        user_settings = UserSettings(user_id=current_user.id)
        db.add(user_settings)
        
    if settings_in.theme is not None:
        user_settings.theme = settings_in.theme
    if settings_in.email_notifications is not None:
        user_settings.email_notifications = settings_in.email_notifications
    if settings_in.ats_threshold is not None:
        user_settings.ats_threshold = settings_in.ats_threshold
        
    db.commit()
    db.refresh(user_settings)
    return {"message": "Settings updated successfully", "theme": user_settings.theme}

@router.post("/change-password")
def change_password(
    pwd_in: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(pwd_in.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password entered is incorrect"
        )
        
    current_user.hashed_password = hash_password(pwd_in.new_password)
    db.commit()
    return {"message": "Password changed successfully"}

@router.delete("/delete-account")
def delete_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db.delete(current_user)
    db.commit()
    return {"message": "Account deleted successfully"}
