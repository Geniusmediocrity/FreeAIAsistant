import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.methods import DeleteWebhook
import requests

from settings.correct_messages import CorrectMessages

from settings.read_files import read_file

from settings.DB_connect import DataBase

from settings.buttons import Buttons
from settings.config import Config
from settings.messages import Messages



logging.basicConfig(level=logging.INFO)

bot = Bot(Config.TELEGRAM_TOKEN)
dp = Dispatcher()    
DB = DataBase(database="db/DataBase.db") #? коннект с БД


#? Базовые команды:
@dp.message(CommandStart())
async def command_start(message: types.Message):
    """⁡⁢⁣⁣Начало использования"""
    DB.start_db_model(user_id=message.from_user.id)
    await message.reply(text=Messages.START_MESSAGE, parse_mode = 'HTML')

@dp.message(Command("restart"))
async def cmd_start(message: types.Message):
    """⁡⁢⁣⁣Команда start"""
    DB.start_db_model(user_id=message.from_user.id)
    await message.reply(text=Messages.RESTART_MESSAGE, parse_mode = 'HTML')

    
@dp.message(Command("help"))
async def help(message: types.Message):
    """Команда help"""
    await message.reply(text=Messages.HELP_MESSAGE, parse_mode="HTML")
    

@dp.message(Command("info"))
async def info(message: types.Message):
    """Получить информацию о боте"""
    await message.reply(text=Messages.INFO_MESSAGE, parse_mode="HTML")


#! ------ Обработка команд выбора/просмотра моделей -----
#? Посмотреть используемую модель:
@dp.message(Command("model"))
async def get_model(message: types.Message):
    """Посмотреть выбранную модель"""
    model = DB.read_db_model(user_id=message.from_user.id)
    await message.reply(text=f"Текущая модель: {model}", parse_mode="HTML")
    
@dp.message(Command("visualmodel"))
async def get_visualmodel(message: types.Message):
    visual_model = DB.read_db_visualmodel(user_id=message.from_user.id)
    await message.reply(text=f"Текущая модель для работы с фото: {visual_model}", parse_mode="HTML")
    
    
#? Выбор модели использования:
@dp.message(Command("setmodel"))    
async def setmodel(message: types.Message):
    """Выбрать модель для использования"""
    await message.reply(text="Выбери модель:", reply_markup=Buttons.get_inline_keyboard())
    
@dp.message(Command("setvisualmodel"))    
async def setvisualmodel(message: types.Message):
    """Выбрать фото модель для использования"""
    await message.reply(text="Выбери модель:", reply_markup=Buttons.get_setvismodel_keybord())

@dp.callback_query()
async def callback_setmodel(callback: types.CallbackQuery):
    """Кнопки для выбора модели использования"""
    await callback.message.edit_reply_markup(reply_markup=None)
    data = callback.data
    if data != "cancel":
        if data in ["meta-llama/Llama-3.2-90B-Vision-Instruct", "Qwen/Qwen2-VL-7B-Instruct"]:
            DB.update_db_visualmodel(user_id=callback.from_user.id, visualmodel=data)
        else:
            DB.update_db_model(user_id=callback.from_user.id, model=data)
        await callback.message.answer(text=f"Текущая модель: {data}", parse_mode="HTML")
    else:
        await callback.message.answer(text="/cancel", parse_mode="HTML")


#! ---- Очистка истории запросов ----
@dp.message(Command("clear"))
async def clear(message: types.Message):
    DB.clear_db_history(user_id=message.from_user.id)
    await message.reply(text="История запросов успешно очищена 🧹", parse_mode="HTML")
    
    
@dp.message(Command("sendall"))
async def sendall(message: types.Message):
    if message.from_user.id == 7314948275:
        text = message.text[9: ]
        for user_id in DB.get_db_users():
            try:
                await bot.send_message(chat_id=user_id[0], text=text)
            except:
                DB.delete_db_user(user_id=user_id)
        print("Рассылка завершена успешно")
                

#! ---- Сами запросы ----
#? Обработчик текстовых пользовательских запросов
@dp.message(lambda message: message.text)
async def filter_messages(message: types.Message):
    """Обработчик пользовательских запросов:
    Основная функция бота"""
    
    user_id = message.from_user.id
    message_text = message.text
    
    print("-" * 185)
    print(f"{user_id} question: {message_text}") #? для вывода информации о запросе пользователя
    try:
        # Сохраняем вопрос пользователя
        DB.save_db_history(user_id=user_id, role="user", content=message_text)


        process_mes = await message.reply(text=f"Запрос принят, @{message.from_user.username}!\n{Messages.ANSWER_PROCESSING.format("40")}", parse_mode="HTML")


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
        response = requests.post(Config.URL, headers=Config.HEADERS, json=data)
        data = response.json()


        print(f"Response code: {response}") #? вывод информации о статусе выполнения запроса пользователя
        print("-" * 185)

        text = data['choices'][0]['message']['content']
        bot_text = text.split('</think>\n\n')[1] if "</think>" in text else text

        # Сохраняем ответ ИИ
        DB.save_db_history(user_id=user_id, role="assistant", content=text)
        
        await bot.delete_message(chat_id=message.chat.id, message_id=process_mes.message_id)
        
        for text in CorrectMessages.split_message(message=bot_text):
            await message.reply(text, parse_mode="Markdown")
            
    except Exception as e:
        await message.answer(text="Возникла непредвиденная ошибка.\nМы уже стараемся все исправить.\nНапишите в поддержку: @Geniusmediocrity")
        print(e)


#? Обработчик фото пользовательских запросов
@dp.message(lambda message: message.photo)
async def handle_message(message: types.Message):
    """ Обработчик изображений """
    user_id = message.from_user.id
    process_mes = await message.reply(text=f"Запрос принят, @{message.from_user.username}!\n{Messages.ANSWER_PROCESSING.format("60")}", parse_mode="HTML")
    question = CorrectMessages.translate_to_english(text=message.caption) if message.caption else "What is in this image?"
    
    file_id = message.photo[-1].file_id # ⁡⁢⁣⁣Берем фото лучшего качества⁡
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_url = f"https://api.telegram.org/file/bot{Config.TELEGRAM_TOKEN}/{file_path}" # ⁡⁢⁣⁣Получем ссылку на изображение⁡
    
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
        
        response = requests.post(Config.URL, json=data, headers=Config.HEADERS)    
        data = response.json()
        text = CorrectMessages.translate_to_rus(text=data["choices"][0]["message"]["content"]) # ⁡⁢⁣⁣Получаем нужный текст из ⁡⁢⁣⁣JSON файла⁡ и переводим его
        
            
        print(f"Response code: {response}") #? вывод информации о статусе выполнения запроса пользователя
        print("-" * 185)
        
        # Сохраняем ответ ИИ
        DB.save_db_history(user_id=user_id, role="assistant", content=text)
        
        await bot.delete_message(chat_id=message.chat.id, message_id=process_mes.message_id)
        await message.reply(text=text, parse_mode="HTML") # ⁡⁢⁣⁣Отправляем ответ с помощью бота⁡
        
    except Exception as e:
        await message.reply(text="Возникла непредвиденная ошибка.\nМы уже стараемся все исправить.\nНапишите в поддержку: @Geniusmediocrity")
        print(e)
        
        
#? обработчик текстовых документов
@dp.message(lambda message: types.File)
async def handle_document(message: types.Message):
    
    ALLOWED_EXTENSIONS = ['.txt', '.doc', '.docx', ".xml", ".html", ".xlsx", ".csv", ".json"]
    document = message.document

    # Получаем имя файла
    file_name = document.file_name
    process_mes = await message.reply(text=f"Запрос принят, @{message.from_user.username}!\n{Messages.ANSWER_PROCESSING.format("45")}", parse_mode="HTML")

    # Проверяем, что файл имеет допустимое расширение
    if any(file_name.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        # Получаем file_id документа
        file_id = document.file_id

        # Скачиваем файл
        file = await bot.get_file(file_id)
        file_path = file.file_path

        # Полный путь для сохранения файла
        save_path = f"user_files/{file_name}"

        # Скачиваем файл в указанную директорию
        await bot.download_file(file_path=file_path, destination=save_path)

        try:
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            text = read_file(file_path=save_path) # Читаем содержимое файла
            await message.reply(text="Содержимое файла:", parse_mode="HTML")
            
            if file_name.endswith(".xlsx") or file.endswith(".csv"):
                for txt in text:
                    await message.reply(text=txt, parse_mode="HTML") # Отправляем содержимое пользователю
                    
            else:
                for txt in CorrectMessages.split_message(text):
                    await message.reply(text=txt, parse_mode="HTML") # Отправляем содержимое пользователю
                
        except Exception as e:
            await message.reply(text="Возникла непредвиденная ошибка.\nМы уже стараемся все исправить.\nНапишите в поддержку: @Geniusmediocrity", parse_mode="HTML")
            print(e)
    else:
        # Если расширение не разрешено, сообщаем об ошибке
        await message.reply(text="Пожалуйста, отправьте файл в формате .txt, .doc или .docx.", parse_mode="HTML")
    await bot.delete_message(chat_id=message.chat.id, message_id=process_mes.message_id)


async def main():
    """Главный скрипт"""
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
