from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from cognicube_backend.databases.database import get_db
from cognicube_backend.models.user import User
from cognicube_backend.services.ai_chat import ai_chat_api, create_conversation_record
from cognicube_backend.utils.jwt_generator import get_jwt_token_user_id
from cognicube_backend.schemas.conversation import (
    ConversationRequest,
    ConversationResponse,
)

ai = APIRouter(prefix="/apis/v1/ai")


@ai.post("/conversation", response_model=ConversationResponse)
async def create_conversation(
    message: ConversationRequest,
    user_id: int = Depends(get_jwt_token_user_id),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    ai_response = await ai_chat_api(message.message)
    create_conversation_record(db, user_id, message.message, ai_response)
    return {"reply": ai_response}
