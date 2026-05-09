from sqlalchemy import Column, String, Boolean, JSON, DateTime
from app.models.base import BaseModel


class Reminder(BaseModel):
    __tablename__ = "reminders"

    user_id = Column(String, nullable=False, index=True)
    family_member_id = Column(String, nullable=True)
    title = Column(String(200), nullable=False)
    type = Column(String(30), nullable=True)
    schedule = Column(JSON, default=dict)
    next_trigger = Column(DateTime, nullable=True)
    enabled = Column(Boolean, default=True)
