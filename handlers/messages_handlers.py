import logging

from aiogram import Router
from aiogram import types

from configs import DB
from settings.messages import Messages
from utils.correct_messages import CorrectMessages


# TODO: Накинуть декораторы db и Requests и CorrectMessages


messages_router = Router(name=__name__)

#? Обработчик текстовых пользовательских запросов
@messages_router.message(lambda message: message.text)
async def handle_messages(message: types.Message):
    """Обработчик пользовательских запросов:
    Основная функция бота"""
    
    user_id = message.from_user.id
    message_text = message.text
    
    print("-" * 185)
    print(f"{user_id} question: {message_text}") #? для вывода информации о запросе пользователя
    # try:
    # Сохраняем вопрос пользователя
    DB.save_db_history(user_id=user_id, role="user", content=message_text)
    process_mes = await message.reply(text=Messages.ANSWER_PROCESSING.format(message.from_user.username, "50"), parse_mode="HTML")
    model = DB.read_db_model(user_id=user_id)
    
    # Загружаем историю диалога
    messages = DB.load_db_history(user_id)
    messages.insert(0, {"role": "system", "content": "Ты очень полезный высокоуровневый помощник"})
    messages.append({"role": "user", "content": message_text})
    
    # запрос к API
    data = {
        "model": model,
        "messages": messages
    }
    response = requests.post(URL, headers=HEADERS, json=data)
    data = response.json()
    
    print(f"Response    code: {response}") #? вывод информации о статусе выполнения запроса пользователя
    print("-" * 185)
    text = data['choices'][0]['message']['content']
    bot_text = text.split('</think>\n\n')[1] if "</think>" in text else text
    
    # Сохраняем ответ ИИ
    DB.save_db_history(user_id=user_id, role="assistant", content=text)
    
    await bot.delete_message(chat_id=message.chat.id, message_id=process_mes.message_id)
    
    for text in CorrectMessages.split_message(message=bot_text):
        await message.reply(text, parse_mode="Markdown")
        
    # except Exception as e:
    # logging.exception(f"Ошибка в handle_messages: {e}")
    # await message.answer(text=Messages.ERROR_MESSAGE)
    # print(e)
