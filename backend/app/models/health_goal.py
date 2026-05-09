from sqlalchemy import Column, String, Date, JSON, Float
from app.models.base import BaseModel


class HealthGoal(BaseModel):
    __tablename__ = "health_goals"

    user_id = Column(String, nullable=False, index=True)
    family_member_id = Column(String, nullable=True)
    title = Column(String(200), nullable=False)
    category = Column(String(30), nullable=True)
    target = Column(JSON, default=dict)
    target_value = Column(Float, nullable=True)
    current_value = Column(Float, nullable=True)
    unit = Column(String(20), nullable=True)
    progress = Column(JSON, default=dict)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    status = Column(String(20), default="active")
