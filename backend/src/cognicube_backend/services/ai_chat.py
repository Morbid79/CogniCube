import aiohttp
from fastapi import HTTPException, status
from cognicube_backend.models.conversation import Conversation, Who
from sqlalchemy.orm import Session
from cognicube_backend.config import CONFIG

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
