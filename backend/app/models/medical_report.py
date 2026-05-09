from sqlalchemy import Column, String, Text, Date, JSON
from app.models.base import BaseModel


class MedicalReport(BaseModel):
    __tablename__ = "medical_reports"

    user_id = Column(String, nullable=False, index=True)
    family_member_id = Column(String, nullable=True)
    title = Column(String(200), default="体检报告")
    hospital = Column(String(200), nullable=True)
    report_date = Column(Date, nullable=True)
    source_type = Column(String(20), default="image")  # image | pdf
    source_urls = Column(JSON, default=list)
    raw_text = Column(Text, nullable=True)
    overall_light = Column(String(10), default="green")  # red | yellow | blue | green
    summary = Column(Text, nullable=True)
    action_plan = Column(JSON, nullable=True)
    status = Column(String(20), default="processing")  # processing | completed | failed
