import logging

from aiogram import Router
from aiogram import types
from aiogram.filters import Command

from configs import DB
from settings.messages import Messages


hist_router = Router(name=__name__)

@hist_router.message(Command("clear"))
async def clear(message: types.Message):
    try:
        DB.clear_db_history(user_id=message.from_user.id)
        await message.reply(text="История запросов успешно очищена 🧹", parse_mode="HTML")
    except Exception as e:
        await message.answer(text=Messages.ERROR_MESSAGE)
        logging.exception(f"Ошибка в clear: {e}")