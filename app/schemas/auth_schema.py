from pydantic import BaseModel, EmailStr,  field_validator
from typing import Literal

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    team_id: int | None = None

@field_validator("password")
@classmethod
def validate_password(cls, v: str):
    if len(v) < 6:
        raise ValueError("Password must be at least 6 characters")
    if len(v.encode("utf-8")) > 72:
        raise ValueError("Password too long (max 72 characters)")
    return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    role: str


class ChatOnboardRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Literal["salesman", "manager", "senior_manager", "ceo"]
    team_id: int
