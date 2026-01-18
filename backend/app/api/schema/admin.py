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


class CSVFile(BaseModel):
    filename: str
    size: int
    uploaded_at: str


class CSVFilesResponse(BaseModel):
    success: bool
    error: str | None = None
    files: List[CSVFile]


class CSVDataResponse(BaseModel):
    success: bool
    error: str | None = None
    headers: List[str]
    data: List[List[str]]
    total_rows: int
    page: int
    page_size: int
