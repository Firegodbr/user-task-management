from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException, status, Query, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from app.db.db import get_session
from app.db.user import add_user, get_username
from app.models.refresh_tokens import RefreshToken
from app.models.user import User as UserModel
from app.core.security import hash_token, create_refresh_token, create_csrf, verify_csrf, create_access_token, hash_password
from app.core.lockout import (
    record_login_attempt,
    handle_failed_login,
    handle_successful_login,
    check_account_locked
)
from app.core.audit import AuditLogger
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.api.schema.auth import User, RegisterRequest, ResponseBoolean
from app.core.settings import settings
from app.utils.auth import authenticate_user, get_current_user
from datetime import timedelta, datetime, timezone
from loguru import logger
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter(tags=["Auth"])
limiter = Limiter(key_func=get_remote_address)


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/15minutes")
async def register_user(request: Request, form_data: RegisterRequest = Depends(RegisterRequest.as_form), db: AsyncSession = Depends(get_session)):
    client_ip = request.client.host if request.client else "unknown"

    exist_user = await get_username(db, form_data.username)
    if exist_user:
        raise HTTPException(detail="User already exists", status_code=400)

    user = await add_user(db, form_data.username, hash_password(form_data.password))

    # Audit log registration
    AuditLogger.registration(user.username, client_ip)

    return user


@router.get("/check-user-exists", response_model=ResponseBoolean)
async def check_user_exists(username: str = Query(..., description="Username for check"), db: AsyncSession = Depends(get_session)):
    try:
        user = await get_username(db, username)
        return ResponseBoolean(message=user is not None, success=True)
    except SQLAlchemyError as se:
        logger.error(str(se))
        raise HTTPException(detail=str(
            se), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(detail=str(
            e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/token")
@limiter.limit("5/15minutes")
async def login_for_access_token(
    request: Request,
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_session),
):
    # Get client IP address
    client_ip = request.client.host if request.client else "unknown"

    # First, check if user exists to determine lockout status
    user_check = await get_username(db, form_data.username)

    # Check if account is locked BEFORE attempting authentication
    if user_check:
        is_locked, lock_message = await check_account_locked(user_check)
        if is_locked:
            # Record failed attempt due to lockout
            await record_login_attempt(db, form_data.username, False, client_ip)
            AuditLogger.login_failure(form_data.username, client_ip, reason="account_locked")
            logger.warning(f"Login attempt for locked account: {form_data.username} from {client_ip}")
            raise HTTPException(status_code=423, detail=lock_message)  # 423 Locked

    # Attempt authentication
    user = await authenticate_user(db, form_data.username, form_data.password)

    if not user:
        # Record failed login attempt
        await record_login_attempt(db, form_data.username, False, client_ip)
        AuditLogger.login_failure(form_data.username, client_ip, reason="invalid_credentials")

        # Handle failed login (increment counter, lock if needed)
        if user_check:
            await handle_failed_login(db, user_check, client_ip)

            # Check if this failure caused a lockout
            is_locked, lock_message = await check_account_locked(user_check)
            if is_locked:
                logger.warning(f"Account locked: {form_data.username} due to too many failed attempts")
                raise HTTPException(status_code=423, detail=lock_message)

        raise HTTPException(status_code=401, detail="Incorrect credentials")

    # Successful login - record it and reset failed attempts
    await record_login_attempt(db, form_data.username, True, client_ip)
    await handle_successful_login(db, user)
    user_agent = request.headers.get("user-agent", "unknown")
    AuditLogger.login_success(user.username, client_ip, user_agent)
    logger.info(f"Successful login: {user.username} from {client_ip}")

    # ---- CLEANUP OLD TOKENS ----
    # Delete only expired tokens for this user (keep revoked for audit)
    now = datetime.now(timezone.utc)
    result = await db.execute(
        select(RefreshToken).where(
            RefreshToken.user_id == user.id,
        )
    )
    old_tokens = result.scalars().all()

    for token in old_tokens:
        # Delete only if expired
        expires_at = token.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        if expires_at < now:
            await db.delete(token)

    await db.commit()

    # ---- ACCESS TOKEN (JWT) ----
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    # ---- REFRESH TOKEN (OPAQUE) ----
    raw_refresh_token = create_refresh_token()
    refresh_token_hash = hash_token(raw_refresh_token)

    refresh_token_db = RefreshToken(
        user_id=user.id,
        token_hash=refresh_token_hash,
        expires_at=datetime.now(timezone.utc)
        + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )

    db.add(refresh_token_db)
    await db.commit()

    # ---- COOKIES ----
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    response.set_cookie(
        key="refresh_token",
        value=raw_refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )

    csrf_token = create_csrf()

    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=False,   # so JS can read it
        secure=True,      # only over HTTPS
        samesite="strict",  # prevents cross-site sending
        path="/",         # available for all endpoints
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh", dependencies=[Depends(verify_csrf)])
@limiter.limit("10/minute")
async def refresh_token(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_session),

):
    # 1️⃣ Read refresh token from cookie
    raw_refresh_token = request.cookies.get("refresh_token")
    if not raw_refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    token_hash = hash_token(raw_refresh_token)

    # 2️⃣ Load refresh token from DB
    result = await db.execute(
        select(RefreshToken).where(RefreshToken.token_hash == token_hash)
    )
    stored_token: RefreshToken | None = result.scalar_one_or_none()

    # Token not found → invalid / reused
    if not stored_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # 3️⃣ Check revoked / expired
    now = datetime.now(timezone.utc)
    # Handle timezone-naive expires_at from DB
    expires_at = stored_token.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if stored_token.revoked_at is not None or expires_at < now:
        # 🚨 Possible token reuse → revoke all sessions for this user
        # Audit log security incident
        client_ip = request.client.host if request.client else "unknown"
        user_obj = await db.get(UserModel, stored_token.user_id)
        if user_obj:
            AuditLogger.token_reuse_detected(user_obj.username, client_ip)

        result = await db.execute(
            select(RefreshToken).where(
                RefreshToken.user_id == stored_token.user_id,
                RefreshToken.revoked_at.is_(None),
            )
        )
        tokens = result.scalars().all()
        for token in tokens:
            token.revoked_at = now

        await db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # 4️⃣ Load user
    user = await db.get(UserModel, stored_token.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # 5️⃣ ROTATE refresh token
    new_refresh_token = create_refresh_token()
    new_refresh_token_hash = hash_token(new_refresh_token)

    new_db_token = RefreshToken(
        user_id=user.id,
        token_hash=new_refresh_token_hash,
        expires_at=datetime.now(timezone.utc)
        + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )

    db.add(new_db_token)

    # Flush to get the new token ID
    await db.flush()

    # Revoke old token
    stored_token.revoked_at = datetime.now(timezone.utc)
    stored_token.replaced_by_token_id = new_db_token.id

    # Cleanup only expired tokens for this user (keep revoked for audit)
    result = await db.execute(
        select(RefreshToken).where(
            RefreshToken.user_id == user.id,
        )
    )
    all_tokens = result.scalars().all()

    for token in all_tokens:
        # Skip the new token we just created
        if token.id == new_db_token.id:
            continue

        # Delete only if expired
        expires_at = token.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        if expires_at < now:
            await db.delete(token)

    await db.commit()

    # 6️⃣ Issue new access token (JWT)
    access_token = create_access_token(
        data={
            "sub": user.username,
            "role": user.role,
        },
        expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    )

    # 7️⃣ Set new refresh cookie
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="strict",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/",
    )

    new_csrf_token = create_csrf()
    response.set_cookie(
        key="csrf_token",
        value=new_csrf_token,
        httponly=False,   # JS needs to read it
        secure=settings.COOKIE_SECURE,
        samesite="strict",
        path="/",
    )

    # Audit log token refresh
    client_ip = request.client.host if request.client else "unknown"
    AuditLogger.token_refresh(user.username, client_ip)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=User, dependencies=[Depends(get_current_user)])
async def get_current_user_info(
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    """
    Returns the current authenticated user's information.
    Used by frontend to verify authentication status.
    """
    return User(
        id=current_user.id,
        username=current_user.username,
        role=current_user.role,
        disabled=current_user.disabled
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_csrf), Depends(get_current_user)])
async def logout(
    request: Request,
    response: Response,
    current_user: Annotated[UserModel, Depends(get_current_user)],
    db: AsyncSession = Depends(get_session)
):
    client_ip = request.client.host if request.client else "unknown"

    raw_refresh_token = request.cookies.get("refresh_token")

    if raw_refresh_token:
        token_hash = hash_token(raw_refresh_token)

        result = await db.execute(
            select(RefreshToken)
            .where(
                RefreshToken.token_hash == token_hash,
                RefreshToken.revoked_at.is_(None),
            )
        )
        token = result.scalar_one_or_none()

        if token:
            token.revoked_at = datetime.now(timezone.utc)
            await db.commit()

    AuditLogger.logout(current_user.username, client_ip)

    # Remove cookies (idempotent)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    response.delete_cookie("csrf_token")

    return



