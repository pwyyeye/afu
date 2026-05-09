from sqlalchemy import Column, String, Numeric, JSON, Text
from app.models.base import BaseModel


class HealthProfile(BaseModel):
    __tablename__ = "health_profiles"

    user_id = Column(String, unique=True, nullable=False, index=True)
    blood_type = Column(String(10), nullable=True)
    height_cm = Column(Numeric(5, 1), nullable=True)
    weight_kg = Column(Numeric(5, 1), nullable=True)
    allergies = Column(JSON, default=list)
    chronic_conditions = Column(JSON, default=list)
    medications = Column(JSON, default=list)
    surgical_history = Column(JSON, default=list)
    family_history = Column(JSON, default=list)
    smoking = Column(String(20), nullable=True)
    drinking = Column(String(20), nullable=True)
    exercise_freq = Column(String(20), nullable=True)
    notes = Column(Text, nullable=True)
