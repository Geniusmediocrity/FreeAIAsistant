import logging

from aiogram import Router
from aiogram import types
from aiogram.filters import CommandStart, Command

from configs import DB
from utils.messages import Messages
from utils.decorators import msg_handler


base_router = Router(name=__name__)


@base_router.message(CommandStart())
@msg_handler
async def command_start(message: types.Message):
    """Start using"""
    try:
        DB.start_db_model(user_id=message.from_user.id)
        await message.reply(text=Messages.START_MESSAGE, parse_mode = 'HTML')
    except Exception as e:
        await message.answer(text=Messages.ERROR_MESSAGE)
        logging.exception(f"Ошибка в command_start: {e}")

@base_router.message(Command("restart"))
@msg_handler
async def command_restart(message: types.Message):
    """⁡⁢⁣Comand start"""
    try:
        DB.start_db_model(user_id=message.from_user.id)
        await message.reply(text=Messages.RESTART_MESSAGE, parse_mode = 'HTML')
    except Exception as e:
        await message.answer(text=Messages.ERROR_MESSAGE)
        logging.exception(f"Ошибка в command_restart: {e}")

    
@base_router.message(Command("help"))
@msg_handler
async def help(message: types.Message):
    """Comand help"""
    try:
        await message.reply(text=Messages.HELP_MESSAGE, parse_mode="HTML")
    except Exception as e:
        await message.answer(text=Messages.ERROR_MESSAGE)
        logging.exception(f"Ошибка в help: {e}")
    

@base_router.message(Command("info"))
@msg_handler
async def info(message: types.Message):
    """Take info about bot"""
    try:
        await message.reply(text=Messages.INFO_MESSAGE, parse_mode="HTML")
    except Exception as e:
        await message.answer(text=Messages.ERROR_MESSAGE)
        logging.exception(f"Ошибка в info: {e}")