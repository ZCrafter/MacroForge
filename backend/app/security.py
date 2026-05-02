from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.hash import argon2
from .config import settings

ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["argon2"])
    print("HASHING:", repr(password))   # log plaintext
    h = pwd_context.hash(password)
    print("HASH RESULT:", repr(h))      # so you can see it
    return h

def verify_password(password: str, hashed: str) -> bool:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["argon2"])
    print("VERIFYING PASSWORD:", repr(password))
    print("VERIFYING AGAINST HASH:", repr(hashed))
    ok = pwd_context.verify(password, hashed)
    print("VERIFY RESULT:", ok)
    return ok

def create_access_token(sub: str, expires_minutes: int = 60 * 24 * 7) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    return jwt.encode({"sub": sub, "exp": exp}, settings.jwt_secret_key, algorithm=ALGORITHM)

def decode_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[ALGORITHM])
        return payload.get("sub")
    except Exception:
        return None
