from aiogram import Router
from aiogram import types
from aiogram import F

from utils.decorators import msg_handler

from configs import bot

from utils.messages import Messages

from utils.ai_requests import send_ai_request
from utils.correct_messages import CorrectMessages


messages_router = Router(name=__name__)


@messages_router.message(F.text)
@msg_handler
async def handle_messages(message: types.Message):
    """Handler of users requests:
    Main bot function"""
    process_mes = await message.reply(text=Messages.ANSWER_PROCESSING.format(message.from_user.username, "50"), parse_mode="HTML")
    bot_answer = await send_ai_request(message_text=message.text, user_id=message.from_user.id)

    await bot.delete_message(chat_id=message.chat.id, message_id=process_mes.message_id)

    for chunk in CorrectMessages.split_message(message=bot_answer):
        await message.reply(chunk, parse_mode="Markdown")
        
        
