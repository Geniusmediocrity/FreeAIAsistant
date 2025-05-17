from aiogram import Router
from aiogram import types
from aiogram import F

from utils.messages import Messages
from utils.correct_messages import CorrectMessages
from utils.decorators import msg_handler
from utils.ai_requests import send_ai_request
from configs import bot, __TELEGRAM_TOKEN


# TODO: use db
# TODO: use Requests
# TODO: use CorrectMessages
# TODO: Change func
# TODO: Make a note: 
# Requirement	         |  Details
# -----------------------+----------------------------------------------------
# Format	             |  JPEG, PNG, WEBP, or GIF (static)
# Max File Size	         |  20MB
# Resolution	         |  At least 512x512 pixels recommended
# Max Dimensions	     |  4096×4096 pixels
# Accessibility	         |  If using a URL, ensure it is publicly accessible
# Multi-Image Support	 |  Up to 10 images per request




photo_router = Router(name=__name__)


@photo_router.message(F.photo)
@msg_handler
async def handle_photo(message: types.Message):
    """Users photo handler 20MB"""
    user_id = message.from_user.id
    caption = message.caption
    
    process_mes = await message.reply(text=Messages.ANSWER_PROCESSING.format(message.from_user.username, "60"), parse_mode="HTML")
    
    question = CorrectMessages.translate_text(text=caption) if caption else "What is in this image?"
    
    file_id = message.photo[-1].file_id # take the best quality photos
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_url = f"https://api.telegram.org/file/bot{__TELEGRAM_TOKEN}/{file_path}"

    data = [
                {"type": "text", "text": question},
                {"type": "image_url", "image_url": {"url": file_url}}
            ]
    
    result = await send_ai_request(message_text=data, user_id=user_id, request_type="visualmodel")
    text = CorrectMessages.translate_text(text=result)
    
    await process_mes.delete()
    await message.reply(text=text, parse_mode="HTML")