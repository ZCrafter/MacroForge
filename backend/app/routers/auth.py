from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user
from ..models import User
from ..schemas import LoginIn, Token
from ..security import verify_password, create_access_token
from ..config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"access_token": create_access_token(user.username), "token_type": "bearer"}

@router.get("/me")
def me(user: str = Depends(get_current_user)):
    return {"username": user, "authenticated": True}

@router.get("/debug")
def debug():
    return {
        "admin_username_env": settings.admin_username,
        "admin_password_length": len(settings.admin_password),
        "password_set": bool(settings.admin_password),
    }
