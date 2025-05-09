import asyncio
from aiogram.methods import DeleteWebhook

from configs import bot, dp
from logs.events_logging import setup_logger
from handlers import main_handler_router

  
  
dp.include_router(main_handler_router)


async def main():
    """Главный скрипт"""
    setup_logger()
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
