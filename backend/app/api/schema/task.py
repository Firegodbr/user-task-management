from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from typing import List, Optional, Annotated


class TaskElement(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    task: str
    date: date


class TaskListResponse(BaseModel):
    success: bool
    tasks: List[TaskElement]
    total: int = 0  # Total number of tasks
    page: int = 1  # Current page number
    page_size: int = 10  # Number of items per page
    total_pages: int = 0  # Total number of pages
    error: str | None = None


class TaskResponse(BaseModel):
    success: bool
    task: TaskElement | None = None
    error: str | None = None


class TaskPost(BaseModel):
    desc: Annotated[str, Field(description="Task description", min_length=1)]
    date: Annotated[date, Field(description="Due date")]
