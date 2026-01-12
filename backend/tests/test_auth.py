from httpx import AsyncClient
import jwt
from app.core.settings import settings
from loguru import logger
async def test_register_call(async_client: AsyncClient):
    """Test call to endpoint for creating a user"""
    response = await async_client.post(
        "/auth/register",
        data={"username": "testuser", "password": "password123!"}
    )

    assert response.status_code == 201
    assert response.json()["username"] == "testuser"

    response = await async_client.post(
        "/auth/register",
        data={"username": "testuser", "password": "password123!"}
    )

    assert response.status_code == 400


async def test_login_call(async_client: AsyncClient, create_user_with_task):
    user, task = await create_user_with_task()
    response = await async_client.post(
        "/auth/token",
        data={"username": user.username, "password": "password123!"}
    )
    assert response.status_code == 200
    # Parse response as JSON
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    access_token = data["access_token"]

    payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["sub"] == "testuser"
    assert "role" in payload

    # You can also check expiration exists
    assert "exp" in payload