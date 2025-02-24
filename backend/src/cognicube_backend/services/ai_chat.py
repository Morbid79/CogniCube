import aiohttp
from fastapi import HTTPException, status
from cognicube_backend.config import CONFIG

async def ai_chat_api(user_message: str) -> str:
    """调用DeepSeek API的函数"""
    SESSION = aiohttp.ClientSession()
    try:
        async with SESSION.post(
            CONFIG.AI_API_URL,
            headers={
                "Authorization": f"Bearer {CONFIG.AI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "messages": [{"role": "user", "content": user_message}],
                "model": "deepseek-ai/DeepSeek-V3",
                "temperature": 0.7
            }
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return data["choices"][0]["message"]["content"]

    except aiohttp.ClientError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"AI服务请求失败: {str(e)}")
