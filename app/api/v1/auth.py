from fastapi import APIRouter, Depends, HTTPException, status, Response, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.core.deps import get_current_user
from app.models.user import User, UserSettings
from app.schemas.user import UserCreate, UserResponse, Token, UserLogin

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, response: Response, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_in.email.lower()).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists"
        )
    
    hashed_pwd = hash_password(user_in.password)
    new_user = User(
        full_name=user_in.full_name,
        email=user_in.email.lower(),
        hashed_password=hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Initialize default settings
    default_settings = UserSettings(user_id=new_user.id, theme="dark")
    db.add(default_settings)
    db.commit()
    db.refresh(new_user)

    # Auto-login token
    access_token = create_access_token(data={"sub": str(new_user.id)})
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True, max_age=86400 * 7)

    return new_user

@router.post("/login", response_model=Token)
def login(
    response: Response,
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == login_data.email.lower()).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is deactivated"
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True, max_age=86400 * 7)

    return Token(access_token=access_token, token_type="bearer")

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
