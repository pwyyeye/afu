import uuid
import json
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage
from app.schemas.chat import (
    ChatSessionCreate, ChatSessionResponse,
    ChatMessageCreate, ChatMessageResponse,
)
from app.services.llm_service import llm_service
from app.core.exceptions import NotFoundException

router = APIRouter()

HEALTH_QA_SYSTEM = """你是阿福，一位专业、友好的AI健康助手。你的职责是：
1. 用通俗易懂的语言回答用户的健康问题
2. 主动追问以了解更多信息，给出更准确的建议
3. 对于严重症状，强烈建议用户及时就医
4. 绝不进行诊断，始终声明你的建议仅供参考
5. 保持温暖、关怀的语气

请始终在回答末尾提醒：以上内容仅供参考，不构成医疗建议，如有不适请及时就医。"""


@router.get("/sessions", response_model=List[ChatSessionResponse])
def list_sessions(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    sessions = (
        db.query(ChatSession)
        .filter(ChatSession.user_id == str(user.id))
        .order_by(ChatSession.updated_at.desc())
        .all()
    )
    result = []
    for s in sessions:
        last_msg = (
            db.query(ChatMessage)
            .filter(ChatMessage.session_id == str(s.id))
            .order_by(ChatMessage.created_at.desc())
            .first()
        )
        result.append(ChatSessionResponse(
            id=str(s.id),
            title=s.title or "新的咨询",
            last_message=last_msg.content[:50] if last_msg else None,
            family_member_id=s.family_member_id,
            created_at=s.created_at,
            updated_at=s.updated_at,
        ))
    return result


@router.post("/sessions", response_model=ChatSessionResponse)
def create_session(
    data: ChatSessionCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = ChatSession(
        id=str(uuid.uuid4()),
        user_id=str(user.id),
        family_member_id=data.family_member_id,
        title="新的咨询",
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return ChatSessionResponse(
        id=str(session.id),
        title=session.title,
        family_member_id=session.family_member_id,
        created_at=session.created_at,
        updated_at=session.updated_at,
    )


@router.delete("/sessions/{session_id}")
def delete_session(
    session_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id, ChatSession.user_id == str(user.id))
        .first()
    )
    if not session:
        raise NotFoundException("会话不存在")

    db.query(ChatMessage).filter(ChatMessage.session_id == session_id).delete()
    db.delete(session)
    db.commit()
    return {"success": True}


@router.get("/sessions/{session_id}/messages", response_model=List[ChatMessageResponse])
def get_messages(
    session_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )
    return [
        ChatMessageResponse(
            id=str(m.id),
            session_id=str(m.session_id),
            role=m.role,
            content=m.content,
            content_type=m.content_type,
            media_url=m.media_url,
            created_at=m.created_at,
        )
        for m in messages
    ]


def _build_messages(db: Session, session_id: str, user_content: str) -> list:
    history = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )
    messages = [{"role": "system", "content": HEALTH_QA_SYSTEM}]
    for msg in history[-10:]:
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": user_content})
    return messages


@router.post("/messages")
def send_message(
    data: ChatMessageCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Save user message
    user_msg = ChatMessage(
        id=str(uuid.uuid4()),
        session_id=data.session_id,
        role="user",
        content=data.content,
        content_type=data.content_type,
    )
    db.add(user_msg)

    # Update session title
    session = db.query(ChatSession).filter(ChatSession.id == data.session_id).first()
    if session and session.title == "新的咨询":
        session.title = data.content[:30]

    db.commit()

    # Build LLM messages
    messages = _build_messages(db, data.session_id, data.content)

    # Get AI response (non-streaming fallback)
    ai_content = llm_service.chat(messages, temperature=0.7)

    # Save AI response
    ai_msg = ChatMessage(
        id=str(uuid.uuid4()),
        session_id=data.session_id,
        role="assistant",
        content=ai_content,
        content_type="text",
    )
    db.add(ai_msg)
    db.commit()

    return {"content": ai_content, "message_id": str(ai_msg.id)}


@router.post("/messages/stream")
def send_message_stream(
    data: ChatMessageCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """SSE streaming endpoint for real-time AI responses."""

    # Save user message
    user_msg = ChatMessage(
        id=str(uuid.uuid4()),
        session_id=data.session_id,
        role="user",
        content=data.content,
        content_type=data.content_type,
    )
    db.add(user_msg)

    # Update session title
    session = db.query(ChatSession).filter(ChatSession.id == data.session_id).first()
    if session and session.title == "新的咨询":
        session.title = data.content[:30]

    db.commit()

    # Build LLM messages
    messages = _build_messages(db, data.session_id, data.content)

    # Create placeholder AI message
    ai_msg_id = str(uuid.uuid4())

    def generate():
        full_content = []
        try:
            for chunk in llm_service.chat_stream(messages, temperature=0.7):
                full_content.append(chunk)
                yield f"data: {json.dumps({'type': 'chunk', 'content': chunk}, ensure_ascii=False)}\n\n"

            # Save complete AI response
            complete_content = "".join(full_content)
            ai_msg = ChatMessage(
                id=ai_msg_id,
                session_id=data.session_id,
                role="assistant",
                content=complete_content,
                content_type="text",
            )
            db.add(ai_msg)
            db.commit()

            yield f"data: {json.dumps({'type': 'done', 'message_id': ai_msg_id}, ensure_ascii=False)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/messages/image")
async def send_image_message(
    session_id: str = "",
    file: UploadFile = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Handle image message - analyze with vision model."""
    import base64

    if not file:
        return {"content": "未收到图片", "message_id": str(uuid.uuid4())}

    content_bytes = await file.read()
    image_base64 = base64.b64encode(content_bytes).decode("utf-8")

    # Save user image message
    user_msg = ChatMessage(
        id=str(uuid.uuid4()),
        session_id=session_id,
        role="user",
        content="[图片]",
        content_type="image",
    )
    db.add(user_msg)

    # Analyze image with vision model
    prompt = "请描述这张图片的内容。如果这是医疗相关的图片（如体检报告、药品说明、病历等），请进行专业解读。"
    try:
        ai_content = llm_service.analyze_image(image_base64, prompt)
    except Exception as e:
        ai_content = f"图片分析失败: {str(e)}"

    # Save AI response
    ai_msg = ChatMessage(
        id=str(uuid.uuid4()),
        session_id=session_id,
        role="assistant",
        content=ai_content,
        content_type="text",
    )
    db.add(ai_msg)
    db.commit()

    return {"content": ai_content, "message_id": str(ai_msg.id)}


@router.post("/messages/voice")
async def send_voice_message(
    session_id: str = "",
    file: UploadFile = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Handle voice message - transcribe and respond."""
    import base64

    if not file:
        return {"content": "未收到语音", "message_id": str(uuid.uuid4())}

    content_bytes = await file.read()

    # For now, treat voice as a text question
    # In production, use DashScope ASR or Qwen audio model for transcription
    # Placeholder: ask user to type instead
    user_msg = ChatMessage(
        id=str(uuid.uuid4()),
        session_id=session_id,
        role="user",
        content="[语音消息]",
        content_type="voice",
    )
    db.add(user_msg)

    ai_content = "我已收到您的语音消息。目前语音识别功能正在开发中，请暂时使用文字描述您的健康问题，我会尽力为您解答。"

    ai_msg = ChatMessage(
        id=str(uuid.uuid4()),
        session_id=session_id,
        role="assistant",
        content=ai_content,
        content_type="text",
    )
    db.add(ai_msg)
    db.commit()

    return {"content": ai_content, "message_id": str(ai_msg.id)}
