import logging

from aiogram import Router
from aiogram import types

from settings.messages import Messages
from utils.correct_messages import CorrectMessages
from configs import DB, bot, TELEGRAM_TOKEN


# TODO: Накинуть декораторы db и Requests и CorrectMessages


photo_router = Router(name=__name__)

#? Обработчик фото пользовательских запросов
@photo_router.message(lambda message: message.photo)
async def handle_message(message: types.Message):
    """ Обработчик изображений """
    user_id = message.from_user.id
    process_mes = await message.reply(text=Messages.ANSWER_PROCESSING.format(message.from_user.username, "60"), parse_mode="HTML")
    question = CorrectMessages.translate_to_english(text=message.caption) if message.caption else "What is in this image?"
    
    file_id = message.photo[-1].file_id # ⁡⁢⁣⁣Берем фото лучшего качества⁡
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}" # ⁡⁢⁣⁣Получем ссылку на изображение⁡
    
    print("-" * 185)
    print(f"{user_id} photo: {file_url}\nquestion: {question}") #? для вывода информации о запросе пользователя
    try:
        # Сохраняем вопрос пользователя
        DB.save_db_history(user_id=user_id, role="user", content=f"Photo: {file_url}. {question}")
        
        
        # запрос к API
        visual_model = DB.read_db_visualmodel(user_id=user_id)
        data = {
            "model": visual_model, 
            "messages": [
                {"role": "system", 
                "content": "You're a helpful AI assistant"},
                
                {"role": "user", 
                "content": [
                    {"type": "text", "text": question},
                    {"type": "image_url", "image_url": {"url": file_url}}
                ]
                }
            ]
        }
        
        response = requests.post(URL, json=data, headers=HEADERS)    
        data = response.json()
        text = CorrectMessages.translate_to_rus(text=data["choices"][0]["message"]["content"]) # ⁡⁢⁣⁣Получаем нужный текст из ⁡⁢⁣⁣JSON файла⁡ и переводим его
        
            
        print(f"Response code: {response}") #? вывод информации о статусе выполнения запроса пользователя
        print("-" * 185)
        
        # Сохраняем ответ ИИ
        DB.save_db_history(user_id=user_id, role="assistant", content=text)
        
        await bot.delete_message(chat_id=message.chat.id, message_id=process_mes.message_id)
        await message.reply(text=text, parse_mode="HTML") # ⁡⁢⁣⁣Отправляем ответ с помощью бота⁡
        
    except Exception as e:
        logging.exception(f"Ошибка в handle_message: {e}")
        await message.reply(text=Messages.ERROR_MESSAGE)
        print(e)