from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from .db import SessionLocal
from .security import decode_token

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request):
    auth = request.headers.get("authorization", "")
    token = auth.replace("Bearer ", "").strip()
    user = decode_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user
