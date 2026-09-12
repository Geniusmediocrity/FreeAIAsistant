import asyncio
from aiogram.methods import DeleteWebhook

from configs import bot, dp, DB
from logs.events_logging import setup_logger
from handlers import main_handler_router

  
  
dp.include_router(main_handler_router)


async def main():
    """Main script"""
    # try:
    setup_logger()
    await DB.connect()
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)
    await DB.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
