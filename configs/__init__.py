import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher

from db import DataBase


load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
__AI_TOKEN = os.getenv("AI_TOKEN")
URL = os.getenv('URL')
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {__AI_TOKEN}"
}


bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher()
DB = DataBase()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')