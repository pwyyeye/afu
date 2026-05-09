from typing import Optional
from fastapi import Depends, Header
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.core.security import verify_token
from app.core.exceptions import UnauthorizedException
from app.models.user import User


def get_current_user(
    authorization: Optional[str] = Header(None, alias="Authorization"),
    db: Session = Depends(get_db),
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthorizedException()
    token = authorization[7:]
    user_id = verify_token(token)
    if not user_id:
        raise UnauthorizedException("Token无效或已过期")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UnauthorizedException("用户不存在")
    return user
