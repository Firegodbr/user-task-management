from pydantic import BaseModel, ConfigDict
from typing import List


class UserOut(BaseModel):
    id: int
    username: str
    role: str
    disabled: bool
    model_config = ConfigDict(from_attributes=True)


class UsersResponse(BaseModel):
    success: bool
    error: str | None = None
    users: List[UserOut]
