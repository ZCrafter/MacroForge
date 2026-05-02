from fastapi.middleware.cors import CORSMiddleware
from .api import app
from .db import Base, engine, SessionLocal
from .models import User, UserProfile
from .security import hash_password
from .config import settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == settings.admin_username).first()
        if not user:
            user = User(username=settings.admin_username, password_hash=hash_password(settings.admin_password))
            db.add(user)
            db.commit()
            db.refresh(user)
            db.add(UserProfile(user_id=user.id))
            db.commit()
    finally:
        db.close()
