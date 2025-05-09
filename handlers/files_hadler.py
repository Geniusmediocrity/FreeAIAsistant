from aiogram import Router
from aiogram import types

from configs import bot

from utils.messages import Messages
from utils.read_files import read_file
from utils.correct_messages import CorrectMessages
from utils.ai_requests import send_ai_request
from utils.decorators import msg_handler


files_router = Router(name=__name__)

@files_router.message(lambda message: types.File)
@msg_handler
async def handle_document(message: types.Message):
    """Text documents handler"""
    document = message.document

    file_name = document.file_name
    process_mes = await message.reply(text=Messages.ANSWER_PROCESSING.format(message.from_user.username, "45"), parse_mode="HTML")

    file_id = document.file_id    
    file = await bot.get_file(file_id)
    file_path = file.file_path

    save_path = f"user_files/{file_name}"
    await bot.download_file(file_path=file_path, destination=save_path)
    
    text = read_file(file_path=save_path)

    data = await send_ai_request(message_text=text)

    text = data['choices'][0]['message']['content']
    bot_answer = text.split('</think>\n\n')[1] if "</think>" in text else text
                
    await bot.delete_message(chat_id=message.chat.id, message_id=process_mes.message_id)
    
    for chunk in CorrectMessages.split_message(message=bot_answer):
        await message.reply(chunk, parse_mode="Markdown")
