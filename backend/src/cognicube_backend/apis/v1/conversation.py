import os
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime, UTC

from cognicube_backend.databases.database import get_db
from cognicube_backend.models.user import User
from cognicube_backend.models.conversation import Conversation, Who
from cognicube_backend.services.ai_chat import ai_chat_api
from cognicube_backend.utils.jwt_generator import get_jwt_token_user_id

ai = APIRouter(prefix="/apis/v1/ai")

class ConversationRequest(BaseModel):
    message: str = Field(..., min_length=1, description="对话内容")

class ConversationResponse(BaseModel):
    reply: str = Field(..., description="AI生成的回复内容")

class HistoryItem(BaseModel):
    message: str
    reply: str
    timestamp: int

class HistoryResponse(BaseModel):
    history: List[HistoryItem]

def create_conversation_record(db: Session, user_id: int, user_message: str, ai_reply: str):
    """创建对话记录"""
    try:
        user_message_record = Conversation(
            user_id=user_id, message=user_message, who=Who.USER
        )
        db.add(user_message_record)
        db.commit()
        db.refresh(user_message_record)

        ai_message_record = Conversation(
            user_id=user_id, message=ai_reply, who=Who.AI, reply_to=user_message_record.message_id
        )
        db.add(ai_message_record)
        db.commit()
        db.refresh(ai_message_record)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"对话记录保存失败: {str(e)}")

@ai.post("/conversation", response_model=ConversationResponse)
async def create_conversation(
    message: ConversationRequest,
    user_id: int = Depends(get_jwt_token_user_id),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    ai_response = await ai_chat_api(message.message)
    # create_conversation_record(db, request.user_id, request.message, ai_response)
    return {"reply": ai_response}

