from sqlalchemy import Column, String, Text, Date, JSON
from app.models.base import BaseModel


class HealthDiary(BaseModel):
    __tablename__ = "health_diaries"

    user_id = Column(String, nullable=False, index=True)
    family_member_id = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    mood = Column(String(20), nullable=True)
    tags = Column(JSON, default=list)
    metrics = Column(JSON, default=dict)
    diary_date = Column(Date, nullable=False, index=True)
