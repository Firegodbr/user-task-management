from .db import Task, User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete
from sqlalchemy.future import select
from app.api.schema.task import TaskPost
from loguru import logger
from typing import Optional
from datetime import date

async def get_task(db: AsyncSession, task_id: int) -> Optional[Task]:
    result = await db.execute(select(Task).filter(Task.id == task_id))
    return result.scalars().first()

async def add_task(db: AsyncSession, user_id: int, task_desc: str, task_date: date) -> Task:
    try:
        selected_user = await db.execute(select(User).filter(User.id == user_id))
        user = selected_user.scalars().first()
        if user is None:
            raise ValueError("User not found")
        new_task = Task(task=task_desc, date=task_date, user_id=user.id)
        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)
        return new_task
    except Exception as e:
        logger.error(f"Failed to add task for user_id {user_id}: {e}")
        await db.rollback()  # Rollback in case of error
        raise


async def put_task(db: AsyncSession, task_id: int, task: TaskPost) -> bool:
    task_db = await get_task(db, task_id)

    await db.execute(
        update(Task)
        .where(Task.id == task_id)
        .values(task=task.desc, date=task.date)
    )
    await db.commit()
    await db.refresh(task_db)
    return task_db


async def delete_task(db: AsyncSession, task_id: int) -> bool:
    await db.execute(delete(Task).where(Task.id == task_id))
    await db.commit()
    return True
