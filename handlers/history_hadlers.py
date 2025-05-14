from aiogram import Router
from aiogram import types
from aiogram.filters import Command

from configs import DB
from utils.decorators import msg_handler


hist_router = Router(name=__name__)

@hist_router.message(Command("clear"))
@msg_handler
async def clear(message: types.Message):
    """Clear DataBase history"""
    DB.clear_history(user_id=message.from_user.id)
    await message.reply(text="История запросов успешно очищена 🧹", parse_mode="HTML")