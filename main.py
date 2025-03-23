import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.methods import DeleteWebhook
import requests

from settings.correct_messages import split_message
from settings.translate import translate_to_rus, translate_to_english

from settings.db_model import start_db_model, read_db_model, update_db_model, read_db_visualmodel, update_db_visualmodel
from settings.db_history import save_db_history, load_db_history, clear_db_history

from settings.buttons import get_inline_keyboard, get_setvismodel_keybord
from settings.tokn import TELEGRAM_TOKEN, URL, HEADERS
from settings.messages import START_MESSAGE, RESTART_MESSAGE, HELP_MESSAGE, ANSWER_PROCESSING, INFO_MESSAGE



logging.basicConfig(level=logging.INFO)
bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher()    


#? Базовые команды:
@dp.message(CommandStart())
async def command_start(message: types.Message):
    """⁡⁢⁣⁣Начоло использования"""
    start_db_model(f"@{message.from_user.username}")
    await message.reply(text=START_MESSAGE, parse_mode = 'HTML')

@dp.message(Command("restart"))
async def cmd_start(message: types.Message):
    """⁡⁢⁣⁣Команда start"""
    start_db_model(f"@{message.from_user.username}")
    await message.reply(text=RESTART_MESSAGE, parse_mode = 'HTML')

    
@dp.message(Command("help"))
async def help(message: types.Message):
    """Команда help"""
    await message.reply(text=HELP_MESSAGE, parse_mode="HTML")
    

@dp.message(Command("info"))
async def info(message: types.Message):
    """Получить информацию о боте"""
    await message.reply(text=INFO_MESSAGE, parse_mode="HTML")


#! ------ Обработка команд выбора/просмотра моделей -----
#? Посмотреть используемую модель:
@dp.message(Command("model"))
async def get_model(message: types.Message):
    """Посмотреть выбранную модель"""
    model = read_db_model(username=f"@{message.from_user.username}")
    await message.reply(text=f"Текущая модель: {model}", parse_mode="HTML")
    
@dp.message(Command("visualmodel"))
async def get_visualmodel(message: types.Message):
    visual_model = read_db_visualmodel(username=f"@{message.from_user.username}")
    await message.reply(text=f"Текущая модель для работы с фото: {visual_model}", parse_mode="HTML")
    
    
#? Выбор модели использования:
@dp.message(Command("setmodel"))    
async def setmodel(message: types.Message):
    """Выбрать модель для использования"""
    await message.reply(text="Выбери модель:", reply_markup=get_inline_keyboard())
    
@dp.message(Command("setvisualmodel"))    
async def setvisualmodel(message: types.Message):
    """Выбрать фото модель для использования"""
    await message.reply(text="Выбери модель:", reply_markup=get_setvismodel_keybord())

@dp.callback_query()
async def callback_setmodel(callback: types.CallbackQuery):
    """Кнопки для выбора модели использования"""
    await callback.message.edit_reply_markup(reply_markup=None)
    data = callback.data
    if data != "cancel":
        if data in ["meta-llama/Llama-3.2-90B-Vision-Instruct", "Qwen/Qwen2-VL-7B-Instruct"]:
            update_db_visualmodel(username=f"@{callback.from_user.username}", visualmodel=data)
        else:
            update_db_model(username=f"@{callback.from_user.username}", model=data)
        await callback.message.answer(text=f"Текущая модель: {data}", parse_mode="HTML")
    else:
        await callback.message.answer(text="/cancel", parse_mode="HTML")


#! ---- Очистка истории запросов ----
@dp.message(Command("clear"))
async def clear(message: types.Message):
    clear_db_history(username=f"@{message.from_user.username}")
    await message.reply(text="История запросов успешно очищена 🧹", parse_mode="HTML")
    


#! ---- Сами запросы ----
#? Обработчик текстовых пользовательских запросов
@dp.message(lambda message: message.text)
async def filter_messages(message: types.Message):
    """Обработчик пользовательских запросов:
    Основная функция бота"""
    
    username = f"@{message.from_user.username}"
    message_text = message.text
    
    print("-" * 185)
    print(f"{username} question: {message_text}") #? для вывода информации о запросе пользователя
    try:
        # Сохраняем вопрос пользователя
        save_db_history(username=username, role="user", content=message_text)


        process_mes = await message.reply(text=f"Запрос принят, @{username}!\n{ANSWER_PROCESSING}", parse_mode="HTML")


        model = read_db_model(username=username)
        # Загружаем историю диалога
        messages = load_db_history(username)
        messages.insert(0, {"role": "system", "content": "Ты очень полезный высокоуровневый помощник"})
        messages.append({"role": "user", "content": message_text})
        
        # запрос к API
        data = {
            "model": model,
            "messages": messages
        }
        response = requests.post(URL, headers=HEADERS, json=data)
        data = response.json()


        print(f"Response code: {response}") #? вывод информации о статусе выполнения запроса пользователя
        print("-" * 185)

        text = data['choices'][0]['message']['content']
        bot_text = text.split('</think>\n\n')[1] if "</think>" in text else text

        # Сохраняем ответ ИИ
        save_db_history(username=username, role="assistant", content=text)
        await bot.delete_message(chat_id=message.chat.id, message_id=process_mes.message_id)
        for text in split_message(message=bot_text):
            await message.reply(text, parse_mode="Markdown")
            
    except Exception as e:
        await message.answer(text="Возникла непредвиденная ошибка.\nМы уже стараемся все исправить.\nНапишите в поддержку: @Geniusmediocrity")
        print(e)


#? Обработчик фото пользовательских запросов
@dp.message(lambda message: message.photo)
async def handle_message(message: types.Message):
    """ Обработчик изображений """
    
    username = f"@{message.from_user.username}"
    question = translate_to_english(text=message.text) if message.text else "What is in this image?"
    process_mes = await message.reply(text=f"Запрос принят, {username}!\n{ANSWER_PROCESSING}", parse_mode="HTML")
    
    file_id = message.photo[-1].file_id # ⁡⁢⁣⁣Берем фото лучшего качества⁡
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}" # ⁡⁢⁣⁣Получем ссылку на изображение⁡
    
    print("-" * 185)
    print(f"{username} photo: {file_url}\nquestion: {question}") #? для вывода информации о запросе пользователя
    
    # запрос к API
    visual_model = read_db_visualmodel(username=username)
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
    text = translate_to_rus(text=data["choices"][0]["message"]["content"]) # ⁡⁢⁣⁣Получаем нужный текст из ⁡⁢⁣⁣JSON файла⁡ и переводим его
    
        
    print(f"Response code: {response}")     #? вывод информации о статусе выполнения запроса пользователя
    print("-" * 185)
    
    await bot.delete_message(chat_id=message.chat.id, message_id=process_mes.message_id)
    await message.reply(text=text, parse_mode="HTML") # ⁡⁢⁣⁣Отправляем ответ с помощью бота⁡



async def main():
    """Главный скрипт"""
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
