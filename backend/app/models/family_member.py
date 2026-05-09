from sqlalchemy import Column, String, Date, JSON
from app.models.base import BaseModel


class FamilyMember(BaseModel):
    __tablename__ = "family_members"

    user_id = Column(String, nullable=False, index=True)
    name = Column(String(50), nullable=False)
    relationship = Column(String(30), nullable=False)
    gender = Column(String(10), nullable=True)
    birth_date = Column(Date, nullable=True)
    phone = Column(String(20), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    health_profile = Column(JSON, default=dict)
