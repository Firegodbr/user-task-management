import hashlib
from app.core.settings import settings
import secrets
from datetime import timedelta, datetime, timezone
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from fastapi import HTTPException, Request, status

# Initialize Argon2 password hasher with secure defaults
ph = PasswordHasher()


def verify_csrf(request: Request):
    csrf_cookie = request.cookies.get("csrf_token")
    csrf_header = request.headers.get("X-CSRF-Token")

    if not csrf_cookie or not csrf_header:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if csrf_cookie != csrf_header:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


def hash_password(password: str) -> str:
    """
    Hash a password using Argon2id algorithm.
    Argon2 is the winner of the Password Hashing Competition and provides
    strong protection against brute-force attacks with adaptive complexity.
    """
    return ph.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against an Argon2 hash.
    Returns True if the password matches, False otherwise.
    """
    try:
        ph.verify(hashed_password, plain_password)

        # Check if the hash needs rehashing (algorithm parameters updated)
        if ph.check_needs_rehash(hashed_password):
            # In production, you should rehash and update the database here
            pass

        return True
    except VerifyMismatchError:
        return False
    except Exception:
        # Handle any other exceptions (invalid hash format, etc.)
        return False


def get_password_hash(password: str) -> str:
    """Alias for hash_password for compatibility."""
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
