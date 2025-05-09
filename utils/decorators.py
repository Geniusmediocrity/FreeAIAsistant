import logging
from functools import wraps

from aiogram import types

from utils.messages import Messages


def msg_handler(func) -> callable:
    """The wrpper what logs hanlers"""
    @wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        try:
            await func(message, *args, **kwargs)
            logging.info(f"@{message.from_user.username}({message.from_user.id}) succes question: \
{message.text or (f'Type: {message.content_type};  Caption: {message.caption}')}")
            
        except Exception as e:
            logging.exception(f"Ошибка в handle_messages: {e}")
            await message.answer(text=Messages.ERROR_MESSAGE)
            
    return wrapper