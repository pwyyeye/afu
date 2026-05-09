from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ChatSessionCreate(BaseModel):
    family_member_id: Optional[str] = None


class ChatSessionResponse(BaseModel):
    id: str
    title: str
    last_message: Optional[str] = None
    family_member_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChatMessageCreate(BaseModel):
    session_id: str
    content: str
    content_type: str = "text"


class ChatMessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    content_type: str
    media_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
