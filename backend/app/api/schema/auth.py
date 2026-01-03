from pydantic import BaseModel, Field, field_validator
import re
from fastapi import Form


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    role: str | None = None
    disabled: bool

    class Config():
        from_attributes = True


class UserInDB(User):
    id: int
    hashed_password: str


class ResponseBoolean(BaseModel):
    message: bool
    error: str | None = None
    success: bool


class RegisterRequest(BaseModel):
    username: str = Field(..., description="Username of the user", json_schema_extra={
                          "example": "john", "examples": ["JohnDoe", "AnaLek"]})
    password: str = Field(..., description="Password of the user", json_schema_extra={
                          "format": "password", "example": "***"})

    @field_validator("username")
    @classmethod
    def username_no_special_chars(cls, username: str):
        if not re.match("[A-Za-z0-9]", username):
            raise ValueError("It shouldn't have special characteres")
        return username

    @field_validator("password")
    @classmethod
    def password_must_have_special_chars(cls, password: str):
        if not re.match("^(?=.*[!@#$%^&*(),.?:|<>]).+$", password):
            raise ValueError("Missing special char on password")
        return password

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        password: str = Form(...),
    ) -> "RegisterRequest":
        return cls(username=username, password=password)


class TokenData(BaseModel):
    username: str | None = None
