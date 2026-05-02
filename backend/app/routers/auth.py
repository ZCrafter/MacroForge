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
    print("LOGIN REQUEST:", data.username, "type of password:", type(data.password))
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        print("USER NOT FOUND:", data.username)
        raise HTTPException(status_code=401, detail="Invalid username or password")
    print("FOUND USER, checking password hash")
    if not verify_password(data.password, user.password_hash):
        print("PASSWORD VERIFY FAILED")
        raise HTTPException(status_code=401, detail="Invalid username or password")
    print("LOGIN OK, creating token")
    return {"access_token": create_access_token(user.username), "token_type": "bearer"}

@router.get("/me")
def me(user: str = Depends(get_current_user)):
    print("AUTHENTICATED USER:", user)
    return {"username": user, "authenticated": True}
