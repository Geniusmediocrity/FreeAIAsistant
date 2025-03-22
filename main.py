import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.methods import DeleteWebhook
import requests

from settings.correct_messages import split_message

from settings.db_model import start_db_model, read_db_model, update_db_model
from settings.db_history import save_db_history, load_db_history, clear_db_history

from settings.buttons import get_inline_keyboard
from settings.tokn import TELEGRAM_TOKEN, AI_TOKN, URL
from settings.messages import START_MESSAGE, RESTART_MESSAGE, HELP_MESSAGE, ANSWER_PROCESSING, INFO_MESSAGE



logging.basicConfig(level=logging.INFO)
bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher()    

model = "deepseek-ai/DeepSeek-R1"


#? Базовые команды:
@dp.message(CommandStart())
async def command_start(message: types.Message):
    """⁡⁢⁣⁣Начоло использования"""
    start_db_model(f"@{message.from_user.username}")
    await message.reply(text=START_MESSAGE, parse_mode = 'HTML')

@dp.message(Command("restart"))
async def cmd_start(message: types.Message):
    """⁡⁢⁣⁣Команда start"""
    start_db_model(f"@{message.from_user.username}")
    await message.reply(text=RESTART_MESSAGE, parse_mode = 'HTML')

    
@dp.message(Command("help"))
async def help(message: types.Message):
    """Команда help"""
    await message.reply(text=HELP_MESSAGE, parse_mode="HTML")
    

@dp.message(Command("info"))
async def info(message: types.Message):
    """Получить информацию о боте"""
    await message.reply(text=INFO_MESSAGE, parse_mode="HTML")


#? Команды свзанные с ИИ:
@dp.message(Command("model"))
async def get_model(message: types.Message):
    """Посмотреть выбранную модель"""
    models = read_db_model(username=f"@{message.from_user.username}")
    await message.reply(text=f"Текущая модель: {model}", parse_mode="HTML")
    
    
#? Выбор модели использования:
@dp.message(Command("setmodel"))    
async def setmodel(message: types.Message):
    """Выбрать модель для использования"""
    await message.reply(text="Выбери модель:", reply_markup=get_inline_keyboard())

@dp.callback_query()
async def callback_setmodel(callback: types.CallbackQuery):
    """Кнопки для выбора модели использования"""
    await callback.message.edit_reply_markup(reply_markup=None)
    data = callback.data
    if data != "cancel":
        await callback.message.answer(text=f"Текущая модель: {data}", parse_mode="HTML")
        update_db_model(username=f"@{callback.from_user.username}", model=data)
    else:
        await callback.message.answer(text="/cancel", parse_mode="HTML")


#? Очистка истории запрсов
@dp.message(Command("clear"))
async def clear(message: types.Message):
    clear_db_history(username=f"@{message.from_user.username}")
    await message.reply(text="История запросов успешно очищена", parse_mode="HTML")


#? Обработчик пользовательских запросов
@dp.message(lambda message: message.text)
async def filter_messages(message: types.Message):
    """Обработчик пользовательских запросов:
    Основная функция бота"""
    username = f"@{message.from_user.username}"
    message_text = message.text
    
    print("-" * 185)
    print(f"{username} question: {message_text}")     #? для вывода информации о запросе пользовател 
    try:
        # Сохраняем вопрос пользователя
        save_db_history(username=username, role="user", content=message_text)

        process_mes = await message.reply(text=f"Запрос принят, @{username}!\n{ANSWER_PROCESSING}", parse_mode="HTML")

        model = read_db_model(username=username)
        # Загружаем историю диалога
        messages = load_db_history(username)
        messages.insert(0, {"role": "system", "content": "Ты очень полезный высокоуровневый помощник"})
        messages.append({"role": "user", "content": message_text})
        # запрос к API
        data = {
            "model": model,
            "messages": messages
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {AI_TOKN}",
        }
        response = requests.post(URL, headers=headers, json=data)
        data = response.json()


        print(f"Response code: {response}")     #? вывод информации о статусе выполнения запроса пользователя
        print("-" * 185)

        text = data['choices'][0]['message']['content']
        bot_text = text.split('</think>\n\n')[1] if "</think>" in text else text

        # Сохраняем ответ ИИ
        save_db_history(username=username, role="assistant", content=text)
        await bot.delete_message(chat_id=message.chat.id, message_id=process_mes.message_id)
        for text in split_message(message=bot_text):
            await message.reply(text, parse_mode="Markdown")
            
    except Exception as e:
        await message.answer(text="Возникла непредвиденная ошибка.\nМы уже стараемся все исправить.\nНапишите в поддержку: @Geniusmediocrity")
        print(e)
        
        
@dp.message(lambda message: message.photo)
async def handle_message(message: types.Message):
    model = "meta-llama/Llama-3.2-90B-Vision-Instruct"
    await message.reply(text="Функция временно недоступна", parse_mode="HTML")



async def main():
    """Главный скрипт"""
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
