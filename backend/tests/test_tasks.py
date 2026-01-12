from fastapi.testclient import TestClient
from loguru import logger

async def test_create_task_without_token(async_client: TestClient):
    response = await async_client.post(
        "/tasks/",
        json={
            "desc": "Test task",
            "date": "2025-01-01",
        },
    )
    assert response.status_code == 401


async def test_create_task_with_token(async_client: TestClient, jwt_token_user, create_user_with_task):
    user, task = await create_user_with_task()
    token = await jwt_token_user(user.username)
    response = await async_client.post(
        "/tasks/",
        json={
            "desc": "Test task",
            "date": "2025-01-01",
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    assert response.status_code == 200


async def test_get_task_with_token(
    async_client,
    create_user_with_task,
    jwt_token_user,
):
    user, task = await create_user_with_task()
    token = await jwt_token_user(sub=user.username)

    response = await async_client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["task"] == "test task"

async def test_get_task_with_token(
    async_client,
    create_user_with_task,
    jwt_token_user,
):
    user, task = await create_user_with_task()
    token = await jwt_token_user(sub=user.username)

    response = await async_client.get(
        f"/tasks/{task.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["task"]["task"] == task.task
    assert data["task"]["id"] == task.id
    assert data["task"]["date"] == str(task.date)