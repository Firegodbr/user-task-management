from .db import Task, User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete
from sqlalchemy.future import select
from loguru import logger
from typing import Optional
from datetime import date
from typing import List


async def add_user(db: AsyncSession, username: str, password: str) -> User:
    new_user = User(username=username, password=password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


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


async def get_tasks(db: AsyncSession, user_id: int) -> List[Task]:
    result = await db.execute(select(Task).filter(Task.user_id == user_id))
    return result.scalars().all()
