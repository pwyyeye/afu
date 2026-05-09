from sqlalchemy import Column, String, Text, Integer, ForeignKey
from app.models.base import BaseModel


class ChatMessage(BaseModel):
    __tablename__ = "chat_messages"

    session_id = Column(String(36), ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # user | assistant | system
    content = Column(Text, nullable=False)
    content_type = Column(String(20), default="text")  # text | image | voice
    media_url = Column(String(500), nullable=True)
    token_count = Column(Integer, nullable=True)
