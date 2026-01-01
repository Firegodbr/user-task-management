from fastapi import Depends, Path, Body, HTTPException, status
from fastapi.routing import APIRouter
from app.db.task import get_task as get_task_db, put_task as put_task_db, delete_task as delete_task_db, add_task as add_task_db
from app.db.db import get_session
from app.api.schema.task import  TaskPost, TaskResponse, TaskElement
from app.api.schema.auth import UserInDB
from typing import Annotated
from app.utils.auth import get_current_user
from loguru import logger
router = APIRouter(tags=["Tasks"])

async def check_task_ownership(db, current_user, id):
    # Log to verify that the ID is being passed correctly
    logger.info(f"Fetching task with ID: {id}")
    task = await get_task_db(db, task_id=id)
    
    # If no task is found, raise a 404 Not Found
    if not task:
        logger.error(f"Task with ID {id} does not exist.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This item does not exist")

    # If the user doesn't own the task, raise a 403 Forbidden
    if task.user_id != current_user.id:
        logger.error(f"User {current_user.id} is not authorized to delete task {id}.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This item does not belong to this user")
    
    return task
    
@router.post("/", response_model=TaskResponse)
async def add_task(current_user: Annotated[UserInDB, Depends(get_current_user)], task_in: TaskPost = Body(...), db=Depends(get_session)):
    try:
        new_task = await add_task_db(
            db=db,
            user_id=current_user.id,
            task_desc=task_in.desc,
            task_date=task_in.date
        )

        return TaskResponse(
            success=True,
            task=TaskElement.model_validate(new_task)
        )
    except ValueError as ve:
        return TaskResponse(success=False, task=None, error=str(ve))
    except Exception as e:
        return TaskResponse(success=False, task=None, error="Internal Server Error")


@router.get("/{id}", response_model=TaskResponse)
async def get_task(current_user: Annotated[UserInDB, Depends(get_current_user)], id: Annotated[int, Path(title="The ID of the item to get", description="The ID must be number")], db=Depends(get_session)):
    task = await check_task_ownership(db, current_user, id)
    try:
        task_response = TaskResponse(task=TaskElement.model_validate(
            task), success=True)
        return task_response
    except ValueError as ve:
        logger.critical(ve)
        return TaskResponse(success=False, task=None, error=str(ve))
    except Exception as e:
        return TaskResponse(success=False, task=None, error="Internal Server Error")


@router.put("/{id}", response_model=TaskResponse)
async def put_task(current_user: Annotated[UserInDB, Depends(get_current_user)], id: Annotated[int, Path(title="The ID of the item to update", description="The ID must be number")], task: TaskPost = Body(...), db=Depends(get_session)):
    await check_task_ownership(db, current_user, id)
    try:
        task = await put_task_db(db, task_id=id, task=task)
        task_response = TaskResponse(
            task=TaskElement.model_validate(task), success=True)
        return task_response
    except ValueError as ve:
        return TaskResponse(success=False, task=None, error=str(ve))
    except Exception as e:
        return TaskResponse(success=False, task=None, error="Internal Server Error")


@router.delete("/{id}", response_model=TaskResponse)
async def delete_task(current_user: Annotated[UserInDB, Depends(get_current_user)], id: Annotated[int, Path(title="The ID of the item to delete", description="The ID must be number")], db=Depends(get_session)):
    task = await check_task_ownership(db, current_user, id)
    try:
        result = await delete_task_db(db, task_id=id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not deleted with success")
        task_response = TaskResponse(
            task=TaskElement.model_validate(task), success=True)
        return task_response
    except ValueError as ve:
        return TaskResponse(success=False, task=None, error=str(ve))
    except Exception as e:
        return TaskResponse(success=False, task=None, error="Internal Server Error")
