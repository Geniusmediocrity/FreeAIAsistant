from aiogram import Router
from aiogram import types
from aiogram.filters import CommandStart, Command

from configs import DB
from utils.messages import Messages
from utils.decorators import msg_handler


base_router = Router(name=__name__)


@base_router.message(CommandStart())
@msg_handler
async def command_start(message: types.Message) -> types.Message:
    """Start using"""
    user_id = message.from_user.id
    if not await DB.is_user_exists(user_id):
        await DB.create_new_user(user_id=message.from_user.id)        
    else:
        await DB.clear_history(user_id)
        await DB.reset_user_settings(user_id)
    await message.reply(text=Messages.START_MESSAGE, parse_mode = 'HTML')
    
    
@base_router.message(Command("restart"))
@msg_handler
async def command_restart(message: types.Message) -> types.Message:
    """⁡⁢⁣Comand restart"""
    user_id = message.from_user.id
    await DB.clear_history(user_id)
    await DB.reset_user_settings(user_id)
    await message.reply(text=Messages.RESTART_MESSAGE, parse_mode = 'HTML')

    
@base_router.message(Command("help"))
@msg_handler
async def help(message: types.Message) -> types.Message:
    """Comand help"""
    await message.reply(text=Messages.HELP_MESSAGE, parse_mode="HTML")
    

@base_router.message(Command("info"))
@msg_handler
async def info(message: types.Message) -> types.Message:
    """Take info about bot"""
    await message.reply(text=Messages.INFO_MESSAGE, parse_mode="HTML", disable_web_page_preview=True)