import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status, Request
from app.db.user import get_username
from app.db.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from typing import Annotated
from app.core.settings import settings
from app.api.schema.auth import TokenData, User
from app.core.security import verify_password, create_access_token as security_create_access_token
from loguru import logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)


async def authenticate_user(db: AsyncSession, username: str, password: str):
    """Authenticate user with username and password."""
    user = await get_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    return user


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    """Create JWT access token using the security module."""
    return security_create_access_token(data, expires_delta)


def decode_jwt(token: str | bytes) -> dict:
    """Decode and validate JWT token."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        # Validate token type
        if payload.get("type") != "access":
            raise InvalidTokenError("Invalid token type")
        return payload
    except ExpiredSignatureError:
        raise InvalidTokenError("Token has expired")


async def get_current_user(
    request: Request,
    token: Annotated[str | None, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_session)]
):
    """
    Get current user from JWT token.
    Supports both:
    - Authorization header (Bearer token) for API clients
    - Cookie-based token for browser clients
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Try to get token from header first, then from cookie
    access_token = token
    if not access_token:
        access_token = request.cookies.get("access_token")

    if not access_token:
        raise credentials_exception

    try:
        payload = decode_jwt(access_token)
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError as e:
        logger.debug(f"Token validation failed: {e}")
        raise credentials_exception

    user = await get_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Ensure the current user is not disabled."""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


