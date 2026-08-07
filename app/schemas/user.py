from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

class UserSettingsUpdate(BaseModel):
    theme: Optional[str] = "dark"
    email_notifications: Optional[bool] = True
    ats_threshold: Optional[int] = 75

class UserSettingsResponse(BaseModel):
    theme: str
    email_notifications: bool
    ats_threshold: int

    model_config = ConfigDict(from_attributes=True)

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    settings: Optional[UserSettingsResponse] = None

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
