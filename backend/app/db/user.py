from app.models.user import User
from app.models.task import Task
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete, func
from sqlalchemy.future import select
from loguru import logger
from typing import List
from app.api.schema.auth import User as UserSchema, UserInDB


async def add_user(db: AsyncSession, username: str, hashed_password: str) -> User:
    new_user = User(username=username, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


async def get_username(db: AsyncSession, username: str) -> UserInDB | None:
    result = await db.execute(select(User).filter(User.username == username))
    user_db = result.scalars().first()
    if not user_db:
        return None

    return UserInDB(username=user_db.username, role=user_db.role, disabled=user_db.disabled, hashed_password=user_db.hashed_password, id=user_db.id, is_locked=user_db.is_locked(), locked_until=user_db.locked_until)


async def put_user_pw(db: AsyncSession, user_id: int, pw: str) -> bool:
    try:
        db_user = get_user(db, user_id)

        if db_user:
            await db.execute(
                update(User).where(User.id == user_id).values(password=pw)
            )
            await db.commit()
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"Failed to update password for user {user_id}: {e}")
        return False


async def delete_user(db: AsyncSession, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        try:
            await db.execute(delete(User).where(User.id == user_id))
            await db.commit()
            return True
        except Exception as e:
            return False
    else:
        return False


async def get_tasks(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 10) -> List[Task]:
    """
    Get paginated tasks for a user, ordered by date ascending.

    Args:
        db: Database session
        user_id: User ID to filter tasks
        skip: Number of records to skip (offset)
        limit: Maximum number of records to return

    Returns:
        List of Task objects
    """
    result = await db.execute(
        select(Task)
        .filter(Task.user_id == user_id)
        .order_by(Task.date.asc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_tasks_count(db: AsyncSession, user_id: int) -> int:
    """
    Get total count of tasks for a user.

    Args:
        db: Database session
        user_id: User ID to filter tasks

    Returns:
        Total number of tasks
    """
    result = await db.execute(
        select(func.count(Task.id))
        .filter(Task.user_id == user_id)
    )
    return result.scalar() or 0

async def get_users(db: AsyncSession) -> List[User]:
    result = await db.execute(select(User))
    return result.scalars().all()