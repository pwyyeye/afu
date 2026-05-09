import uuid
import random
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.core.security import create_access_token, create_refresh_token, verify_token
from app.models.user import User
from app.schemas.auth import (
    SmsCodeRequest, SmsCodeResponse,
    LoginRequest, TokenResponse,
    RefreshRequest, UserResponse,
)
from app.core.exceptions import BadRequestException

router = APIRouter()

# In-memory SMS code store (use Redis in production)
_sms_codes: dict = {}


@router.post("/sms-code", response_model=SmsCodeResponse)
def send_sms_code(req: SmsCodeRequest, db: Session = Depends(get_db)):
    code = f"{random.randint(100000, 999999)}"
    _sms_codes[req.phone] = {"code": code, "expires_at": datetime.utcnow().timestamp() + 300}

    if not code:
        pass

    # In dev mode, print the code
    print(f"[DEV] SMS code for {req.phone}: {code}")
    return SmsCodeResponse(success=True, expires_in=300)


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    # Verify SMS code (dev mode: accept "123456" or the generated code)
    stored = _sms_codes.get(req.phone)
    if req.code != "123456" and (not stored or stored["code"] != req.code):
        raise BadRequestException("验证码错误")

    # Find or create user
    user = db.query(User).filter(User.phone == req.phone).first()
    if not user:
        user = User(
            id=str(uuid.uuid4()),
            phone=req.phone,
            nickname=f"用户{req.phone[-4:]}",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Clean up SMS code
    _sms_codes.pop(req.phone, None)

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse(
            id=str(user.id),
            phone=user.phone,
            nickname=user.nickname or "",
            avatar_url=user.avatar_url or "",
            elder_mode=user.elder_mode or False,
            created_at=user.created_at,
        ),
    )


@router.post("/refresh", response_model=dict)
def refresh_token(req: RefreshRequest, db: Session = Depends(get_db)):
    user_id = verify_token(req.refresh_token, token_type="refresh")
    if not user_id:
        raise BadRequestException("Refresh token无效")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise BadRequestException("用户不存在")

    access_token = create_access_token(data={"sub": str(user.id)})
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }
