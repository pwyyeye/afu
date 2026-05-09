from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, date


class HealthProfileUpdate(BaseModel):
    blood_type: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    allergies: Optional[List[str]] = None
    chronic_conditions: Optional[List[str]] = None
    medications: Optional[List[str]] = None
    surgical_history: Optional[List[str]] = None
    family_history: Optional[List[str]] = None
    smoking: Optional[str] = None
    drinking: Optional[str] = None
    exercise_freq: Optional[str] = None
    notes: Optional[str] = None


class HealthProfileResponse(BaseModel):
    id: str
    blood_type: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    allergies: List[str] = []
    chronic_conditions: List[str] = []
    medications: List[str] = []
    surgical_history: List[str] = []
    family_history: List[str] = []
    smoking: Optional[str] = None
    drinking: Optional[str] = None
    exercise_freq: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class FamilyMemberCreate(BaseModel):
    name: str
    relationship: str
    gender: Optional[str] = None
    birth_date: Optional[date] = None
    phone: Optional[str] = None


class FamilyMemberResponse(BaseModel):
    id: str
    name: str
    relationship: str
    gender: Optional[str] = None
    birth_date: Optional[date] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    health_profile: Dict[str, Any] = {}
    created_at: datetime

    class Config:
        from_attributes = True


class DiaryCreate(BaseModel):
    content: str
    mood: Optional[str] = None
    tags: Optional[List[str]] = None
    metrics: Optional[Dict[str, Any]] = None
    diary_date: date
    family_member_id: Optional[str] = None


class DiaryResponse(BaseModel):
    id: str
    content: str
    mood: Optional[str] = None
    tags: List[str] = []
    metrics: Dict[str, Any] = {}
    diary_date: date
    created_at: datetime

    class Config:
        from_attributes = True


class GoalCreate(BaseModel):
    title: str
    category: Optional[str] = None
    target: Optional[Dict[str, Any]] = None
    target_value: Optional[float] = None
    unit: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    family_member_id: Optional[str] = None


class GoalUpdate(BaseModel):
    progress: Optional[Dict[str, Any]] = None
    target_value: Optional[float] = None
    current_value: Optional[float] = None
    unit: Optional[str] = None
    status: Optional[str] = None


class GoalResponse(BaseModel):
    id: str
    title: str
    category: Optional[str] = None
    target: Dict[str, Any] = {}
    target_value: Optional[float] = None
    current_value: Optional[float] = None
    unit: Optional[str] = None
    progress: Dict[str, Any] = {}
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ReminderCreate(BaseModel):
    title: str
    type: Optional[str] = None
    schedule: Optional[Dict[str, Any]] = None
    family_member_id: Optional[str] = None


class ReminderResponse(BaseModel):
    id: str
    title: str
    type: Optional[str] = None
    schedule: Dict[str, Any] = {}
    next_trigger: Optional[datetime] = None
    enabled: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TimelineItem(BaseModel):
    id: str
    type: str
    title: str
    description: Optional[str] = None
    date: str
