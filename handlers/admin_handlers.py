import logging
import asyncio

from aiogram import Router
from aiogram import types
from aiogram.filters import Command

from configs import DB, bot
from utils.decorators import msg_handler


admin_router = Router(name=__name__)
    
@admin_router.message(Command("sendall"))
@msg_handler
async def sendall(message: types.Message) -> types.Message:
    """Mailing function. only for ADMINS using"""
    
    if message.from_user.id == 7314948275:
        text = message.text[9:]
        for user_id in await DB.get_all_users():
            await send_message_to_user(user_id, text)
            await asyncio.sleep(0.1)
        await message.reply("Рассылка завершена успешно")


async def send_message_to_user(user_id: int, text: str) -> types.Message:
    """Sending message to user, what """
    try:
        await bot.send_message(chat_id=user_id, text=text)
    except Exception:
        await bot.send_message(chat_id= 7314948275,text=f"Пользователь {user_id} был удален в связи с некативностью", parse_mode="HTML")
        logging.info(f"Пользователь {user_id} был удален в связи с некативностью")
        await DB.delete_db_user(user_id=user_id)