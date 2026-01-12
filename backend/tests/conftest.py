from httpx import ASGITransport
from sqlalchemy.orm import sessionmaker
import pytest
from httpx import AsyncClient
import jwt
from datetime import datetime, timezone, timedelta, date
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
)

from server.app import app
from app.core.security import get_password_hash
from app.models.user import User as UserModel
from app.models.task import Task as TaskModel
from app.db.db import Base, get_session
from app.core.settings import settings
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    future=True,
)

AsyncSessionLocal = sessionmaker(
    bind=engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session", autouse=True)
async def create_test_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine_test.dispose()


@pytest.fixture
async def db_session():
    async with engine_test.connect() as connection:
        transaction = await connection.begin()

        async_session = sessionmaker(
            bind=connection,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        async with async_session() as session:
            yield session

        await transaction.rollback()


@pytest.fixture
async def override_get_session(db_session):
    async def _override():
        yield db_session

    app.dependency_overrides[get_session] = _override
    yield
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
async def async_client(override_get_session):
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture
async def auth_client_user(async_client, jwt_token_user):
    token = await jwt_token_user()
    async_client.headers.update(
        {"Authorization": f"Bearer {token}"}
    )
    return async_client


@pytest.fixture
async def create_user_with_task(db_session):
    """
    Fixture to create a user with a task in a test DB.
    Rolls back after each test to keep DB clean.
    """
    async def _create_user_task(
        username: str = "testuser",
        password: str = "password123!",
        role: str = "admin",
        disabled: bool = False,
        task_desc: str = "test task",
        task_date: date = date(2025, 1, 1),
    ):

        # Create user
        user = UserModel(
            username=username,
            hashed_password=get_password_hash(password),
            role=role,
            disabled=disabled,
        )
        db_session.add(user)
        await db_session.flush()

        task = TaskModel(
            task=task_desc,
            date=task_date,
            user_id=user.id,
        )
        db_session.add(task)
        await db_session.flush()

        # Return objects without committing to main DB
        return user, task

    return _create_user_task


@pytest.fixture
async def jwt_token_user():
    async def _create_token(sub: str):
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        payload = {
            "sub": sub,
            "role": "user",
            "exp": expire,
        }
        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            settings.ALGORITHM,
        )

    return _create_token
