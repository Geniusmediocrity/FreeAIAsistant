import logging

from aiogram import Router
from aiogram import types
from aiogram.filters import Command

from configs import DB, bot
from utils.decorators import msg_handler


admin_router = Router(name=__name__)

@admin_router.message(Command("sendall"))
@msg_handler
async def sendall(message: types.Message):
    """Mailing function"""
    if message.from_user.id == 7314948275:
        text = message.text[9: ]
        for user_id in DB.get_db_users():
            try:
                await bot.send_message(chat_id=user_id[0], text=text)
            except Exception:
                await message.reply(text=f"Пользователь {user_id} был удален в связи с некативностью", parse_mode="HTML")
                logging.INFO(f"Пользователь {user_id} был удален в связи с некативностью")
                DB.delete_db_user(user_id=user_id)
        print("Рассылка завершена успешно")