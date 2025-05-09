import aiohttp

from configs import HEADERS, URL # , DB


async def send_ai_request(message_text: str) -> dict:
    """send POST-request for AI API and get JSON-answer."""
    
    model = "deepseek-ai/DeepSeek-R1" # DB.get_db_model(user_id=user_id)
    messages = [] # DB.load_db_history(user_id)
    messages.insert(0, {"role": "system", "content": "Ты очень полезный высокоуровневый помощник"})
    messages.append({"role": "user", "content": message_text})
    
    data = {
        "model": model,
        "messages": messages
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url=URL, json=data, headers=HEADERS) as response:
            if response.status != 200:
                error_text = await response.text()
                raise Exception(f"Ошибка ИИ API: {error_text}")
            return await response.json()
        