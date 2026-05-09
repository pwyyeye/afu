from fastapi import APIRouter
from app.api.v1 import auth, users, chat, reports, health

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router, prefix="/auth", tags=["认证"])
router.include_router(users.router, prefix="/users", tags=["用户"])
router.include_router(chat.router, prefix="/chat", tags=["对话"])
router.include_router(reports.router, prefix="/reports", tags=["报告"])
router.include_router(health.router, prefix="/health", tags=["健康"])
