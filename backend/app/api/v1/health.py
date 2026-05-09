import uuid
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.health_profile import HealthProfile
from app.models.family_member import FamilyMember
from app.models.health_diary import HealthDiary
from app.models.health_goal import HealthGoal
from app.models.reminder import Reminder
from app.models.medical_report import MedicalReport
from app.schemas.health import (
    HealthProfileUpdate, HealthProfileResponse,
    FamilyMemberCreate, FamilyMemberResponse,
    DiaryCreate, DiaryResponse,
    GoalCreate, GoalUpdate, GoalResponse,
    ReminderCreate, ReminderResponse,
    TimelineItem,
)
from app.core.exceptions import NotFoundException

router = APIRouter()


# ── Health Profile ──

@router.get("/profile", response_model=HealthProfileResponse)
def get_profile(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == str(user.id)).first()
    if not profile:
        profile = HealthProfile(id=str(uuid.uuid4()), user_id=str(user.id))
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return HealthProfileResponse(
        id=str(profile.id),
        blood_type=profile.blood_type,
        height_cm=float(profile.height_cm) if profile.height_cm else None,
        weight_kg=float(profile.weight_kg) if profile.weight_kg else None,
        allergies=profile.allergies or [],
        chronic_conditions=profile.chronic_conditions or [],
        medications=profile.medications or [],
        surgical_history=profile.surgical_history or [],
        family_history=profile.family_history or [],
        smoking=profile.smoking,
        drinking=profile.drinking,
        exercise_freq=profile.exercise_freq,
        notes=profile.notes,
    )


@router.put("/profile", response_model=HealthProfileResponse)
def update_profile(
    data: HealthProfileUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == str(user.id)).first()
    if not profile:
        profile = HealthProfile(id=str(uuid.uuid4()), user_id=str(user.id))
        db.add(profile)

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    return HealthProfileResponse(
        id=str(profile.id),
        blood_type=profile.blood_type,
        height_cm=float(profile.height_cm) if profile.height_cm else None,
        weight_kg=float(profile.weight_kg) if profile.weight_kg else None,
        allergies=profile.allergies or [],
        chronic_conditions=profile.chronic_conditions or [],
        medications=profile.medications or [],
        surgical_history=profile.surgical_history or [],
        family_history=profile.family_history or [],
        smoking=profile.smoking,
        drinking=profile.drinking,
        exercise_freq=profile.exercise_freq,
        notes=profile.notes,
    )


# ── Family Members ──

@router.get("/family", response_model=List[FamilyMemberResponse])
def list_family(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    members = db.query(FamilyMember).filter(FamilyMember.user_id == str(user.id)).all()
    return [
        FamilyMemberResponse(
            id=str(m.id), name=m.name, relationship=m.relationship,
            gender=m.gender, birth_date=m.birth_date, phone=m.phone,
            avatar_url=m.avatar_url, health_profile=m.health_profile or {},
            created_at=m.created_at,
        )
        for m in members
    ]


@router.post("/family", response_model=FamilyMemberResponse)
def add_family(
    data: FamilyMemberCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    member = FamilyMember(
        id=str(uuid.uuid4()),
        user_id=str(user.id),
        **data.model_dump(),
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    return FamilyMemberResponse(
        id=str(member.id), name=member.name, relationship=member.relationship,
        gender=member.gender, birth_date=member.birth_date, phone=member.phone,
        avatar_url=member.avatar_url, health_profile=member.health_profile or {},
        created_at=member.created_at,
    )


@router.put("/family/{member_id}", response_model=FamilyMemberResponse)
def update_family(
    member_id: str,
    data: FamilyMemberCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    member = db.query(FamilyMember).filter(
        FamilyMember.id == member_id, FamilyMember.user_id == str(user.id)
    ).first()
    if not member:
        raise NotFoundException("成员不存在")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(member, field, value)
    db.commit()
    db.refresh(member)
    return FamilyMemberResponse(
        id=str(member.id), name=member.name, relationship=member.relationship,
        gender=member.gender, birth_date=member.birth_date, phone=member.phone,
        avatar_url=member.avatar_url, health_profile=member.health_profile or {},
        created_at=member.created_at,
    )


@router.delete("/family/{member_id}")
def delete_family(
    member_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    member = db.query(FamilyMember).filter(
        FamilyMember.id == member_id, FamilyMember.user_id == str(user.id)
    ).first()
    if not member:
        raise NotFoundException("成员不存在")
    db.delete(member)
    db.commit()
    return {"success": True}


# ── Health Diary ──

@router.get("/diary", response_model=List[DiaryResponse])
def list_diaries(
    page: int = 1,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    diaries = (
        db.query(HealthDiary)
        .filter(HealthDiary.user_id == str(user.id))
        .order_by(HealthDiary.diary_date.desc())
        .offset((page - 1) * 20)
        .limit(20)
        .all()
    )
    return [
        DiaryResponse(
            id=str(d.id), content=d.content, mood=d.mood,
            tags=d.tags or [], metrics=d.metrics or {},
            diary_date=d.diary_date, created_at=d.created_at,
        )
        for d in diaries
    ]


@router.post("/diary", response_model=DiaryResponse)
def create_diary(
    data: DiaryCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    diary = HealthDiary(
        id=str(uuid.uuid4()),
        user_id=str(user.id),
        **data.model_dump(),
    )
    db.add(diary)
    db.commit()
    db.refresh(diary)
    return DiaryResponse(
        id=str(diary.id), content=diary.content, mood=diary.mood,
        tags=diary.tags or [], metrics=diary.metrics or {},
        diary_date=diary.diary_date, created_at=diary.created_at,
    )


# ── Health Goals ──

@router.get("/goals", response_model=List[GoalResponse])
def list_goals(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    goals = db.query(HealthGoal).filter(HealthGoal.user_id == str(user.id)).all()
    return [
        GoalResponse(
            id=str(g.id), title=g.title, category=g.category,
            target=g.target or {}, target_value=g.target_value,
            current_value=g.current_value, unit=g.unit,
            progress=g.progress or {},
            start_date=g.start_date, end_date=g.end_date,
            status=g.status, created_at=g.created_at,
        )
        for g in goals
    ]


@router.post("/goals", response_model=GoalResponse)
def create_goal(
    data: GoalCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    goal = HealthGoal(
        id=str(uuid.uuid4()),
        user_id=str(user.id),
        **data.model_dump(),
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return GoalResponse(
        id=str(goal.id), title=goal.title, category=goal.category,
        target=goal.target or {}, target_value=goal.target_value,
        current_value=goal.current_value, unit=goal.unit,
        progress=goal.progress or {},
        start_date=goal.start_date, end_date=goal.end_date,
        status=goal.status, created_at=goal.created_at,
    )


@router.put("/goals/{goal_id}", response_model=GoalResponse)
def update_goal(
    goal_id: str,
    data: GoalUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    goal = db.query(HealthGoal).filter(
        HealthGoal.id == goal_id, HealthGoal.user_id == str(user.id)
    ).first()
    if not goal:
        raise NotFoundException("目标不存在")
    if data.progress is not None:
        goal.progress = data.progress
    if data.target_value is not None:
        goal.target_value = data.target_value
    if data.current_value is not None:
        goal.current_value = data.current_value
    if data.unit is not None:
        goal.unit = data.unit
    if data.status is not None:
        goal.status = data.status
    db.commit()
    db.refresh(goal)
    return GoalResponse(
        id=str(goal.id), title=goal.title, category=goal.category,
        target=goal.target or {}, target_value=goal.target_value,
        current_value=goal.current_value, unit=goal.unit,
        progress=goal.progress or {},
        start_date=goal.start_date, end_date=goal.end_date,
        status=goal.status, created_at=goal.created_at,
    )


@router.delete("/goals/{goal_id}")
def delete_goal(
    goal_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    goal = db.query(HealthGoal).filter(
        HealthGoal.id == goal_id, HealthGoal.user_id == str(user.id)
    ).first()
    if not goal:
        raise NotFoundException("目标不存在")
    db.delete(goal)
    db.commit()
    return {"success": True}


# ── Reminders ──

@router.get("/reminders", response_model=List[ReminderResponse])
def list_reminders(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    reminders = db.query(Reminder).filter(Reminder.user_id == str(user.id)).all()
    return [
        ReminderResponse(
            id=str(r.id), title=r.title, type=r.type,
            schedule=r.schedule or {}, next_trigger=r.next_trigger,
            enabled=r.enabled, created_at=r.created_at,
        )
        for r in reminders
    ]


@router.post("/reminders", response_model=ReminderResponse)
def create_reminder(
    data: ReminderCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    reminder = Reminder(
        id=str(uuid.uuid4()),
        user_id=str(user.id),
        **data.model_dump(),
    )
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return ReminderResponse(
        id=str(reminder.id), title=reminder.title, type=reminder.type,
        schedule=reminder.schedule or {}, next_trigger=reminder.next_trigger,
        enabled=reminder.enabled, created_at=reminder.created_at,
    )


# ── Timeline ──

@router.get("/timeline", response_model=List[TimelineItem])
def get_timeline(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = []

    reports = db.query(MedicalReport).filter(
        MedicalReport.user_id == str(user.id)
    ).order_by(MedicalReport.created_at.desc()).limit(20).all()
    for r in reports:
        items.append(TimelineItem(
            id=str(r.id), type="report",
            title=r.title, description=r.summary[:100] if r.summary else None,
            date=str(r.report_date) if r.report_date else r.created_at.strftime("%Y-%m-%d"),
        ))

    diaries = db.query(HealthDiary).filter(
        HealthDiary.user_id == str(user.id)
    ).order_by(HealthDiary.diary_date.desc()).limit(20).all()
    for d in diaries:
        items.append(TimelineItem(
            id=str(d.id), type="diary",
            title="健康日记", description=d.content[:100],
            date=str(d.diary_date),
        ))

    items.sort(key=lambda x: x.date, reverse=True)
    return items[:30]
