import logging

from aiogram import Router
from aiogram import types

from configs import bot

import settings.messages as Messages

from utils.read_files import read_file
from utils.correct_messages import CorrectMessages


# TODO: Накинуть декораторы db и Requests и CorrectMessages


files_router = Router(name=__name__)

#? обработчик текстовых документов
@files_router.message(lambda message: types.File)
async def handle_document(message: types.Message):
    
    ALLOWED_EXTENSIONS = ['.txt', '.doc', '.docx', ".xml", ".html", ".xlsx", ".csv", ".json"]
    document = message.document

    # Получаем имя файла
    file_name = document.file_name
    process_mes = await message.reply(text=Messages.ANSWER_PROCESSING.format(message.from_user.username, "45"), parse_mode="HTML")

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
            logging.exception(f"Ошибка в handle_document: {e}")
            await message.reply(text=Messages.ERROR_MESSAGE, parse_mode="HTML")
            print(e)
    else:
        # Если расширение не разрешено, сообщаем об ошибке
        await message.reply(text="Пожалуйста, отправьте файл в формате .txt, .doc или .docx.", parse_mode="HTML")
    await bot.delete_message(chat_id=message.chat.id, message_id=process_mes.message_id)
