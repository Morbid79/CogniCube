import aiohttp
from fastapi import HTTPException, status
from cognicube_backend.models.conversation import Conversation, Who
from sqlalchemy.orm import Session
from cognicube_backend.config import CONFIG
from datetime import datetime

async def save_message_record(db: Session, user_id: int, user_message: str, who: str, reply_to: int = None):
    """简化保存对话记录的过程"""
    message_record = Conversation(
        user_id=user_id,
        message=user_message,  
        who=who,
        reply_to=reply_to,
    )
    try:
        db.add(message_record)
        await db.commit()
        await db.refresh(message_record)
        return message_record
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"消息保存失败: {str(e)}")

async def create_conversation_record(db: Session, user_id: int, user_message: str, deepseek_function):
    """创建对话记录，先保存提问，再保存回答"""
    try:
        user_message_record = save_message_record(db, user_id, user_message, Who.USER)
        ai_reply = await ai_chat_api(user_message)
        await save_message_record(db, user_id, ai_reply, Who.AI, reply_to=user_message_record.message_id)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"对话记录保存失败: {str(e)}")


# TODO；修改对话保存到数据库的方法，不要俩个都一起放

async def ai_chat_api(user_message: str) -> str:
    """调用DeepSeek API的函数"""
    SESSION = aiohttp.ClientSession()  # TODO: 优化为单例模式
    try:
        async with SESSION.post(
            CONFIG.AI_API_URL,
            headers={
                "Authorization": f"Bearer {CONFIG.AI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "messages": [{"role": "user", "content": user_message}],
                "model": "deepseek-ai/DeepSeek-V3",
                "temperature": 0.7,
            },
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return data["choices"][0]["message"]["content"]

    except aiohttp.ClientError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI服务请求失败: {str(e)}",
        )
