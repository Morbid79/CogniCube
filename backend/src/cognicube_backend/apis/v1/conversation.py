import os
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List
import aiohttp
from sqlalchemy.orm import Session
from datetime import datetime, UTC

from cognicube_backend.databases.user_database import get_db
from cognicube_backend.models.user import User
from cognicube_backend.models.conversation import Conversation, Who

router = APIRouter(prefix="/apis/v1/ai")

DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")

class ConversationRequest(BaseModel):
    user_id: int = Field(..., description="用户唯一标识符")
    message: str = Field(..., min_length=1, max_length=500, description="对话内容")

class ConversationResponse(BaseModel):
    reply: str = Field(..., description="AI生成的回复内容")

class HistoryItem(BaseModel):
    message: str
    reply: str
    timestamp: int

class HistoryResponse(BaseModel):
    history: List[HistoryItem]

async def query_deepseek_api(user_message: str) -> str:
    """调用DeepSeek API的函数"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                DEEPSEEK_API_URL,
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "messages": [{"role": "user", "content": user_message}],
                    "model": "deepseek-chat",
                    "temperature": 0.7
                }
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return data["choices"][0]["message"]["content"]
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"AI服务请求失败: {str(e)}")

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

@router.post("/conversation", response_model=ConversationResponse)
async def create_conversation(request: ConversationRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    ai_response = await query_deepseek_api(request.message)
    create_conversation_record(db, request.user_id, request.message, ai_response)
    return {"reply": ai_response}

@router.get("/history/{user_id}", response_model=HistoryResponse)
def get_conversation_history(user_id: int, start_time: int, end_time: int, db: Session = Depends(get_db)):
    start_dt = datetime.fromtimestamp(start_time, tz=UTC)
    end_dt = datetime.fromtimestamp(end_time, tz=UTC)
    records = db.query(Conversation).filter(
        Conversation.user_id == user_id,
        Conversation.time >= start_dt,
        Conversation.time <= end_dt
    ).order_by(Conversation.time).all()

    history_items = [
        HistoryItem(
            message=record.message,
            reply=record.reply.message if record.reply else "",
            timestamp=int(record.time.timestamp())
        ) for record in records if record.who == Who.USER
    ]
    return {"history": history_items}
