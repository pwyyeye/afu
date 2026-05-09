from sqlalchemy import Column, String, Text, Integer
from app.models.base import BaseModel


class ReportIndicator(BaseModel):
    __tablename__ = "report_indicators"

    report_id = Column(String, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=True)
    value = Column(String(50), nullable=True)
    unit = Column(String(30), nullable=True)
    reference_range = Column(String(50), nullable=True)
    light = Column(String(10), nullable=False)  # red | yellow | blue | green
    explanation = Column(Text, nullable=True)
    trend = Column(String(20), nullable=True)  # rising | falling | stable
    sort_order = Column(Integer, default=0)
