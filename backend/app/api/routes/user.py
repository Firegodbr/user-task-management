from fastapi.routing import APIRouter
from fastapi import Depends, Path
from typing import Annotated
from app.db.user import get_user as get_user_db
from app.db.db import get_session
from app.api.schema.user import UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter(tags=["User"])


@router.get("/{id}", response_model=UserResponse)
async def get_user(id: Annotated[str, Path(...,title="User ID", description="User ID to get")], db: AsyncSession = Depends(get_session)):
    user = await get_user_db(id)
    if user:
        return UserResponse(username=user.username, success=True)
    else:
        return UserResponse(username=None, success=False, error="User not found")
