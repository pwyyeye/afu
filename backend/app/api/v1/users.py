from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import UserResponse, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_me(user: User = Depends(get_current_user)):
    return UserResponse(
        id=str(user.id),
        phone=user.phone,
        nickname=user.nickname or "",
        avatar_url=user.avatar_url or "",
        elder_mode=user.elder_mode or False,
        created_at=user.created_at,
    )


@router.put("/me", response_model=UserResponse)
def update_me(
    data: UserUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if data.nickname is not None:
        user.nickname = data.nickname
    if data.avatar_url is not None:
        user.avatar_url = data.avatar_url
    if data.elder_mode is not None:
        user.elder_mode = data.elder_mode

    db.commit()
    db.refresh(user)

    return UserResponse(
        id=str(user.id),
        phone=user.phone,
        nickname=user.nickname or "",
        avatar_url=user.avatar_url or "",
        elder_mode=user.elder_mode or False,
        created_at=user.created_at,
    )
