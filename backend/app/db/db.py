from sqlalchemy import Column, Integer, String, Date, ForeignKey, inspect
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.core.settings import settings
from typing import AsyncGenerator
from loguru import logger

engine = create_async_engine(
    url=settings.DATABASE_URL, echo=settings.DEBUG, future=True)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user")
    tasks = relationship("Task", back_populates="user")


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    task = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="tasks")


async def create_db():
    try:
        async with engine.begin() as conn:
            existing_tables = await conn.run_sync(
                lambda sync_conn: inspect(sync_conn).get_table_names()
            )

            if not existing_tables:
                logger.info("Creating database and tables...")
                await conn.run_sync(Base.metadata.create_all)
                logger.info("Database and tables created.")
            else:
                logger.info("Database already exists.")
    except OperationalError as e:
        logger.error(f"Error occurred while creating the database: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise


AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        yield db


