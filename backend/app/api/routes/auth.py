from fastapi.routing import APIRouter
from fastapi import Body, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.db.db import get_session
from app.db.user import add_user
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schema.auth import Token, User, RegisterRequest
from app.core.settings import settings
from app.utils.auth import create_access_token, authenticate_user, get_current_active_user, hash_password
from datetime import timedelta
router = APIRouter(tags=["Auth"])


@router.post("/register", response_model=User)
async def register_user(form_data: Annotated[RegisterRequest, Form()], db: AsyncSession = Depends(get_session)):
    user = await add_user(db, form_data.username, hash_password(form_data.password))
    return user


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
