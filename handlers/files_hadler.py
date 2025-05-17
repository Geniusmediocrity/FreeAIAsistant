from aiogram import Router
from aiogram import types
from aiogram import F

from configs import bot

from utils.messages import Messages
from utils.read_files import read_file
from utils.correct_messages import CorrectMessages
from utils.ai_requests import send_ai_request
from utils.decorators import msg_handler


files_router = Router(name=__name__)

@files_router.message(F.document)
@msg_handler
async def handle_document(message: types.Message):
    """Text documents handler"""
    document = message.document
    
    if not document.file_size < 1024 * 1024 * 5:
        return await message.reply(text=Messages.SIZE_ERROR, parse_mode="HTML")

    file_name = document.file_name
    process_mes = await message.reply(text=Messages.ANSWER_PROCESSING.format(message.from_user.username, "45"), parse_mode="HTML")

    file_id = document.file_id    
    file = await bot.get_file(file_id)
    file_path = file.file_path

    save_path = f"user_files/{file_name}"
    await bot.download_file(file_path=file_path, destination=save_path)
    
    try:
        text = await read_file(file_path=save_path)
    except ValueError:
        await bot.delete_message(chat_id=message.chat.id, message_id=process_mes.message_id)
        return await message.reply(text=Messages.EXPANSION_ERROR, parse_mode="HTML")

    prompt = f"{message.caption}\n{file_path}\n{text}"
    bot_answer = await send_ai_request(message_text=prompt, user_id = message.from_user.id)
                
    await process_mes.delete()
    
    for chunk in CorrectMessages.split_message(message=bot_answer):
        await message.reply(chunk, parse_mode="Markdown")
