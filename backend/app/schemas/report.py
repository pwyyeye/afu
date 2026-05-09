from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date


class ReportUploadResponse(BaseModel):
    report_id: str
    status: str = "processing"


class IndicatorResponse(BaseModel):
    id: str
    name: str
    name_en: Optional[str] = None
    value: Optional[str] = None
    unit: Optional[str] = None
    reference_range: Optional[str] = None
    light: str
    explanation: Optional[str] = None
    trend: Optional[str] = None

    class Config:
        from_attributes = True


class ReportResponse(BaseModel):
    id: str
    title: str
    hospital: Optional[str] = None
    report_date: Optional[date] = None
    overall_light: str
    summary: Optional[str] = None
    indicators: List[IndicatorResponse] = []
    action_plan: Optional[list] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class TrendDataPoint(BaseModel):
    year: str
    value: float


class TrendData(BaseModel):
    name: str
    unit: Optional[str] = None
    data: List[TrendDataPoint]
