from pydantic import BaseModel, Field
from typing import Annotated, Optional


class UserInput(BaseModel):
    user: Annotated[str, Field(..., examples=["roger"],
                               description="Username to create an account")]
    password: Annotated[str, Field(..., examples=[
                                   "afsdg"], description="Password to create an account")]


class UserResponse(BaseModel):
    username: Optional[str] = None
    success: bool
    error: Optional[str] = None
