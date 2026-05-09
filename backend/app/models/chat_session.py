from sqlalchemy import Column, String, ForeignKey
from app.models.base import BaseModel


class ChatSession(BaseModel):
    __tablename__ = "chat_sessions"

    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), default="新的咨询")
    family_member_id = Column(String(36), ForeignKey("family_members.id", ondelete="SET NULL"), nullable=True)
