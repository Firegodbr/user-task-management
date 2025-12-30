from fastapi import Depends, Path, Body
from fastapi.routing import APIRouter
from app.db.task import get_task as get_task_db, put_task as put_task_db, delete_task as delete_task_db, add_task as add_task_db
from app.db.db import get_session
from app.api.schema.task import TaskPost, TaskResponse, TaskElement
from typing import Annotated
router = APIRouter(tags=["Tasks"])


@router.post("/", response_model=TaskResponse)
async def add_task(task_in: TaskPost = Body(...), db=Depends(get_session)):
    try:
        new_task = await add_task_db(
            db=db,
            user_id=task_in.user_id,
            task_desc=task_in.desc,
            task_date=task_in.date
        )

        return TaskResponse(
            success=True,
            user_id=new_task.user_id,
            tasks=TaskElement.model_validate(new_task)
        )
    except ValueError as ve:
        return TaskResponse(success=False, user_id=task_in.user_id, tasks=None, error=str(ve))
    except Exception as e:
        return TaskResponse(success=False, user_id=task_in.user_id, tasks=None, error="Internal Server Error")


@router.get("/{id}", response_model=TaskResponse)
async def get_task(id: Annotated[int, Path(title="The ID of the item to get", description="The ID must be number")], db=Depends(get_session)):
    try:
        task = await get_task_db(db, task_id=id)
        task_response = TaskResponse(task=TaskElement.model_validate(
            task), success=True, user_id=task.user_id)
        return task_response
    except ValueError as ve:
        return TaskResponse(success=False, user_id=None, tasks=None, error=str(ve))
    except Exception as e:
        return TaskResponse(success=False, user_id=None, tasks=None, error="Internal Server Error")


@router.put("/{id}", response_model=TaskResponse)
async def put_task(id: Annotated[int, Path(title="The ID of the item to update", description="The ID must be number")], task: TaskPost = Body(...), db=Depends(get_session)):
    try:
        task = await put_task_db(db, task_id=id)
        task_response = TaskResponse(
            task=TaskElement.model_validate(task), success=True, user_id=None)
        return task_response
    except ValueError as ve:
        return TaskResponse(success=False, user_id=None, tasks=None, error=str(ve))
    except Exception as e:
        return TaskResponse(success=False, user_id=None, tasks=None, error="Internal Server Error")


@router.delete("/{id}", response_model=TaskResponse)
async def delete_task(id: Annotated[int, Path(title="The ID of the item to delete", description="The ID must be number")], db=Depends(get_session)):
    try:
        task = await delete_task_db(db, task_id=id)
        task_response = TaskResponse(
            task=TaskElement.model_validate(task), success=True, user_id=None)
        return task_response
    except ValueError as ve:
        return TaskResponse(success=False, user_id=None, tasks=None, error=str(ve))
    except Exception as e:
        return TaskResponse(success=False, user_id=None, tasks=None, error="Internal Server Error")
