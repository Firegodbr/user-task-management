from fastapi.routing import APIRouter
from fastapi import Body, Depends, Form, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.db.db import get_session
from app.db.user import add_user, get_username
from app.core.security import get_password_hash
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schema.auth import Token, User, RegisterRequest, ResponseBoolean
from app.core.settings import settings
from app.utils.auth import create_access_token, authenticate_user, get_current_active_user
from app.core.security import hash_password
from sqlalchemy.exc import SQLAlchemyError
from datetime import timedelta
from loguru import logger
router = APIRouter(tags=["Auth"])


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(form_data: RegisterRequest = Depends(RegisterRequest.as_form), db: AsyncSession = Depends(get_session)):
    exist_user = await get_username(db, form_data.username)
    if exist_user:
        raise HTTPException(detail="User already exists", status_code=400)
    user = await add_user(db, form_data.username, hash_password(form_data.password))
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
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_session),
) -> Token:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
