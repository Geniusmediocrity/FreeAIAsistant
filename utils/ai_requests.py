import aiohttp

from configs import HEADERS, URL, DB


async def send_ai_request(message_text: str | list[dict], user_id: int, request_type="model") -> str:
    """send POST-request for AI API, get JSON-answer, and commit question and answer on Database"""    
    if request_type == "model":
        model = await DB.get_users_model(user_id=user_id)
    else:
        model = await DB.get_users_visual_model(user_id=user_id)
        
    messages = list(await DB.get_users_history(user_id=user_id))
    messages.insert(0, {"role": "system", "content": "You're a helpful AI assistant"})
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
            data = await response.json()
            
    text = data['choices'][0]['message']['content']
    result = text.split('</think>\n\n')[1] if "</think>" in text else text
    
    messages.append({"role": "asistant", "content": result})
    await DB.update_user_history(user_id=user_id, conversation=messages[1:])
    
    return result



"""   Request Example
[
    {
        "role": "system", 
        "content": "You're a helpful AI assistant"
    }, 
    {
        "role": "user", 
        "content": вопрос
    }, 
    {
        "role": "asistant",
        "content": ответ
    }
]
"""