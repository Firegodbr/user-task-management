from pydantic import BaseModel, Field, field_validator, ConfigDict
import re
from fastapi import Form, status
from fastapi.exceptions import HTTPException


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    role: str | None = None
    disabled: bool
    model_config = ConfigDict(from_attributes=True)


class UserInDB(User):
    id: int
    hashed_password: str
    is_locked: bool = False
    locked_until: str | None = None
    failed_login_attempts: int = 0
    


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
            raise HTTPException(detail="It shouldn't have special characteres",status_code=status.HTTP_400_BAD_REQUEST)
        return username

    @field_validator("password")
    @classmethod
    def password_complexity_check(cls, password: str):
        """
        Enforce strong password requirements:
        - Minimum 12 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character
        """
        if len(password) < 12:
            raise HTTPException(detail="Password must be at least 12 characters long",
                                status_code=status.HTTP_400_BAD_REQUEST)

        if not re.search(r"[A-Z]", password):
            raise HTTPException(detail="Password must contain at least one uppercase letter",
                                status_code=status.HTTP_400_BAD_REQUEST)

        if not re.search(r"[a-z]", password):
            raise HTTPException(detail="Password must contain at least one lowercase letter",
                                status_code=status.HTTP_400_BAD_REQUEST)

        if not re.search(r"\d", password):
            raise HTTPException(detail="Password must contain at least one digit",
                                status_code=status.HTTP_400_BAD_REQUEST)

        if not re.search(r"[!@#$%^&*(),.?:|<>_\-+=\[\]{};'\"\\\/~`]", password):
            raise HTTPException(detail="Password must contain at least one special character (!@#$%^&* etc.)",
                                status_code=status.HTTP_400_BAD_REQUEST)

        # Optional: Check for common weak passwords
        common_passwords = ["Password123!", "Admin123456!", "Welcome123!"]
        if password in common_passwords:
            raise HTTPException(detail="Password is too common. Please choose a stronger password",
                                status_code=status.HTTP_400_BAD_REQUEST)

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
