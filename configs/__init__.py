import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher

from db import DataBase


load_dotenv()

__TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
__AI_TOKEN = os.getenv("AI_TOKEN")
URL = os.getenv('URL')
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {__AI_TOKEN}"
}


bot = Bot(__TELEGRAM_TOKEN)
dp = Dispatcher()

DB = DataBase()