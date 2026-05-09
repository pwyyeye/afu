from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SmsCodeRequest(BaseModel):
    phone: str


class SmsCodeResponse(BaseModel):
    success: bool
    expires_in: int = 300


class LoginRequest(BaseModel):
    phone: str
    code: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: "UserResponse"


class RefreshRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    id: str
    phone: str
    nickname: str
    avatar_url: str
    elder_mode: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    elder_mode: Optional[bool] = None
