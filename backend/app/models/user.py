from sqlalchemy import Column, String, Boolean, JSON
from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    phone = Column(String(20), unique=True, nullable=False, index=True)
    nickname = Column(String(50), default="")
    avatar_url = Column(String(500), default="")
    elder_mode = Column(Boolean, default=False)
    settings = Column(JSON, default=dict)
