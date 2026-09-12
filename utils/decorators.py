import logging
from functools import wraps

from aiogram import types

from utils.messages import Messages


def msg_handler(func: callable) -> callable:
    """The wrapper what logs message and commands handlers"""
    
    @wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        try:
            
            await func(message, *args, **kwargs)
            
            if func.__name__ in ('handle_messages', 'handle_photo', 'handle_document'):
                logging.info(f"@{message.from_user.username}({message.from_user.id}) succes question: \
{message.text or (f'Type: {message.content_type};  Caption: {message.caption}')}")
                
            else:
                logging.info(f"@{message.from_user.username}({message.from_user.id}) succes command: {message.text}")
                
        except Exception as e:
            logging.exception(f"Ошибка в {func.__name__}: {e}")
            await message.answer(text=Messages.ERROR_MESSAGE, parse_mode="HTML")
            
    return wrapper