# [Free AI Asistant](https://t.me/FreeNeuroChat_bot "Telegram bot")
<hr>

## Краткое описание

Это телеграмм бот работающий через официальный *API DeepSeek, Qwen, Ozone, Mistral, microsoft*, а также доступен выбор других ИИ моделей.
Бот **полностью бесплатный**.


<hr>

# Установить все используемые библиотеки: 

* uv pip install aiogram aiohttp aiofiles asyncpg PyPDF2 python-docx pandas dotenv
* uv pip install -r requirements.txt

## Структура Проекта

* Директория [settings](settings/) хранит в себе настройки сообщений, моделей, а также токены для корректной работы тг-бота:

    - [buttons.py](settings/buttons.py) - создание кнопок при выборе моделей(/setmodel)
    - [correct_message.py](settings/correct_message.py) - обрезка сообщения на части не превышающей длинну в 4096 символов и прочие темки для корректирования текста созданного ИИ
    - [DB_connect.py](settings/DB_connect.py) - коннект с бд и взаимодействие с ней
    - [messages.py](settings/messages.py) - сообщения ответы на какие-то определенные команды
    - [config.py](settings/config.py) - токены телеграм-бота и ИИ, ссылка на ИИ, а также заголовок для post-запросов

* Директория db нужна для хранения базы данных, структура которой:

    - таблица users_model(username UNIQUE, model TEXT) - нужна для хранения выбранной пользователем модели
    - таблица chat_history(username TEXT, role TEXT, conten TEXT, timestamp DATETIME DEFAULT) - нужны для хранения пользовательских вопросов и ответов ИИ

<hr>

## Планы для выпуска MVP версии (FreeAIAsist v1.0.0a):

- [x] Создание configs. Переход на dotenv
- [x] Уменьшени main.py
- [x] Создание handlers
- [ ] Переделать на новую СУБД, на PostgreSQL
- [ ] Переделать подключение к СУБД и БД в целом
- [ ] Изменить тип хранения Истории запросов. Хранить в массиве
- [x] Закончить наконец Возможность работы с файлами, а именно с текстом
- [x] Добавить логирование + декоратор/хендлер для логирования хендлеров сообщений
- [x] Добавить нормальное чтение файлов (read_files.py)
- [ ] correct_messages.py
- [ ] photo_hadlers.py
- [ ] models_hadlers.py
- [ ] history_hadlers.py
- [ ] base_hadlers.py
- [ ] admin_hadlers.py

