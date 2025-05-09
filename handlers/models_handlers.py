import logging

from aiogram import Router
from aiogram import types
from aiogram.filters import Command

from utils.buttons import Buttons
from configs import DB
from settings.messages import Messages


models_router = Router(name=__name__)

#? Посмотреть используемую модель:
@models_router.message(Command("model"))
async def get_model(message: types.Message):
    """Посмотреть выбранную модель"""
    try:
        model = DB.read_db_model(user_id=message.from_user.id)
        await message.reply(text=f"Текущая модель: {model}", parse_mode="HTML")
    except Exception as e:
        await message.answer(text=Messages.ERROR_MESSAGE)
        logging.exception(f"Ошибка в model: {e}")
    
@models_router.message(Command("visualmodel"))
async def get_visualmodel(message: types.Message):
    """Посмотреть выбранную модель"""
    try:
        visual_model = DB.read_db_visualmodel(user_id=message.from_user.id)
        await message.reply(text=f"Текущая модель для работы с фото: {visual_model}", parse_mode="HTML")
    except Exception as e:
        await message.answer(text=Messages.ERROR_MESSAGE)
        logging.exception(f"Ошибка в visualmodel: {e}")
    
    
#? Выбор модели использования:
@models_router.message(Command("setmodel"))    
async def setmodel(message: types.Message):
    """Выбрать модель для использования"""
    try:
        await message.reply(text="Выбери модель:", reply_markup=Buttons.get_inline_keyboard())
    except Exception as e:
        await message.answer(text=Messages.ERROR_MESSAGE)
        logging.exception(f"Ошибка в setmodel: {e}")
    
@models_router.message(Command("setvisualmodel"))    
async def setvisualmodel(message: types.Message):
    """Выбрать фото модель для использования"""
    try:
        await message.reply(text="Выбери модель:", reply_markup=Buttons.get_setvismodel_keybord())
    except Exception as e:
        await message.answer(text=Messages.ERROR_MESSAGE)
        logging.exception(f"Ошибка в setvisualmodel: {e}")

@models_router.callback_query()
async def callback_setmodel(callback: types.CallbackQuery):
    """Кнопки для выбора модели использования"""
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
        data = callback.data
        if data != "cancel":
            if data in ["meta-llama/Llama-3.2-90B-Vision-Instruct", "Qwen/Qwen2-VL-7B-Instruct"]:
                DB.update_db_visualmodel(user_id=callback.from_user.id, visualmodel=data)
            else:
                DB.update_db_model(user_id=callback.from_user.id, model=data)
            await callback.message.answer(text=f"Текущая модель: {data}", parse_mode="HTML")
        else:
            await callback.message.answer(text="/cancel", parse_mode="HTML")
    except Exception as e:
        logging.exception(f"Ошибка в callback_setmodel: {e}")