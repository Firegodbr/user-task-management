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
    user_id: int
    tasks: List[TaskElement]
    error: Optional[str] = None

class TaskResponse(BaseModel):
    success: bool
    user_id: Optional[int] = None
    tasks: TaskElement
    error: Optional[str] = None

class TaskPost(BaseModel):
    user_id: Annotated[int, Field(description="The user ID", gt=0)]
    desc: Annotated[str, Field(description="Task description", min_length=1)]
    date: Annotated[date, Field(description="Due date")]
