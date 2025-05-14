from aiogram import Router
from aiogram import types
from aiogram.filters import Command

from configs import DB

from utils.keyboard_utils import Buttons
from utils.decorators import msg_handler


models_router = Router(name=__name__)

#? See using model:

@models_router.message(Command("model"))
@msg_handler
async def get_model(message: types.Message):
    """See using model"""
    model = DB.get_users_model(user_id=message.from_user.id)
    await message.reply(text=f"Текущая модель: {model}", parse_mode="HTML")
    

@models_router.message(Command("visualmodel"))
@msg_handler
async def get_visualmodel(message: types.Message):
    """see using visualmodel"""
    visual_model = DB.get_users_visual_model(user_id=message.from_user.id)
    await message.reply(text=f"Текущая модель для работы с фото: {visual_model}", parse_mode="HTML")
    
    
#? Set model for using:

@models_router.message(Command("setmodel"))  
@msg_handler  
async def setmodel(message: types.Message):
    """Set model for using"""
    await message.reply(text="Выбери модель:", reply_markup=Buttons.get_setmodel_inline_kb())
    
    
@models_router.message(Command("setvisualmodel"))    
@msg_handler
async def setvisualmodel(message: types.Message):
    """Set visual model for using"""
    await message.reply(text="Выбери модель:", reply_markup=Buttons.get_setvismodel_inline_kb())


@models_router.callback_query()
@msg_handler
async def callback_setmodel(callback: types.CallbackQuery):
    """Callback Buttons for set model for using"""
    await callback.message.edit_reply_markup(reply_markup=None)
    data = callback.data
    if data != "cancel":
        if data in ["meta-llama/Llama-3.2-90B-Vision-Instruct", "Qwen/Qwen2-VL-7B-Instruct"]:
            DB.update_users_ai_visual_model(user_id=callback.from_user.id, new_ai_visual_model=data)
        else:
            DB.update_users_ai_model(user_id=callback.from_user.id, new_ai_model=data)
        await callback.message.answer(text=f"Текущая модель: {data}", parse_mode="HTML")
    else:
        await callback.message.answer(text="/cancel", parse_mode="HTML")
