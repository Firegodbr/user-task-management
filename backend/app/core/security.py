import hmac
import hashlib
from app.core.settings import settings
import secrets
from datetime import timedelta, datetime, timezone
import jwt

from fastapi import HTTPException, Request, status


def verify_csrf(request: Request):
    csrf_cookie = request.cookies.get("csrf_token")
    csrf_header = request.headers.get("X-CSRF-Token")

    if not csrf_cookie or not csrf_header:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if csrf_cookie != csrf_header:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


def hash_password(password: str):
    return hmac.new(settings.SECRET_KEY.encode("utf-8"), password.encode("utf-8"), hashlib.sha256).hexdigest()


def verify_password(plain_password: str, hashed_password: str):
    pw = hash_password(plain_password)
    return pw == hashed_password


def get_password_hash(password: str):
    return hash_password(password)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def create_refresh_token() -> str:
    return secrets.token_urlsafe(64)


def create_csrf() -> str:
    return secrets.token_urlsafe(32)


def create_access_token(
    data: dict,
    expires_delta: timedelta,
) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access",
    })

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
