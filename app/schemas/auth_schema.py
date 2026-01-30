from pydantic import BaseModel, EmailStr
from typing import Literal

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str


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
