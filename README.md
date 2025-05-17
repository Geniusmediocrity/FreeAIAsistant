# [Free AI Asistant v1.0.0a](https://t.me/FreeNeuroChat_bot "Telegram bot")(eng)

## Description

This is a Telegram bot built using the official *APIs of DeepSeek, Qwen, Ozone, Mistral, Microsoft*, and more. It also supports the selection of various other AI models.

The bot is **completely free to use**.

---

## Install All Dependencies and Libraries

To install all dependencies, run the following commands:

```bash
cd pyconfig
uv sync --active
```
or
```bash
pip install -r pyconfig/requirements.txt
```

---

## Project Structure

1. **`configs`**
   _This directory contains project configuration files._

   * `__init__.py`: Loads parameters from `.env`, initializes `DataBase`, `bot`, `dispatcher`, and creates `HEADERS` for API requests to AI models. Initializes publick key objects such as:
     - `bot`
     - `dp`
     - `DB`
     - `HEADERS`
   * `.env`: File for storing environment variables (example: API tokens, database connection settings).

2. **`db`**
   _Directory responsible for working with the database._

   - `__init__.py`: Combines the `UserHistory` and `UserSettings` classes into `DataBase`.
   - `db_manager.py`: Core module for managing the database (connection, disconnection). The foundational parent class.
   - `postgres_queries.py`: Contains SQL queries for PostgreSQL.
   - `table_history.py`: Module for working with the user request history table.
   - `table_usersettings.py`: Module for working with the user settings table.

3. **`handlers`**
   _Directory containing event handlers (for a Telegram bot)._

   - `__init__.py`: Creates a `main_handler_router` aiogram.Router object that includes all routers from the `handlers` module.
   - `admin_handlers.py`: Handlers for admin commands: `/sendall`.
   - `base_handlers.py`: Base handlers like `/start`, `/restart`, `/help`, `/info`.
   - `files_handler.py`: Handlers for file messages.
   - `history_handler.py`: Handlers for working with user history: `/clear`.
   - `messages_handlers.py`: Handlers for text messages.
   - `models_handlers.py`: Handlers related to AI models: `/setmodel`, `/model`, `\setvisualmodel`, `\visualmodel` and callback queries.
   - `photo_handlers.py`: Handlers for photo messages.

4. **`logs`**
   _Directory for storing application logs._

   - `__init__.py`: Makes the `logs` directory a Python package.
   - `bot.log`: Log file for recording bot events.
   - `events_logging.py`: Module for configuring and managing event logging.

5. **`pyconfig`**
   _Directory for setting up the development environment and managing dependencies._

   - `.python-version`: Specifies the Python version used in the project.
   - `pyproject.toml`: Configuration file for uv (package manager) or poetry.
   - `requirements.txt`: List of project dependencies.
   - `uv.lock`: Lock file for the uv package manager.

6. **`utils`**
   _Directory containing utility functions and helper modules._

   - `__init__.py`: Makes the `utils` directory a Python package.
   - `ai_requests.py`: Module for asynchronous HTTP requests.
   - `correct_messages.py`: Module for message validation and correction.
   - `decorators.py`: Module for creating decorators (e.g., for logging or error handling).
   - `keyboard_utils.py`: Module for working with keyboards (e.g., for Telegram bots).
   - `messages.py`: Module for storing message templates.
   - `read_files.py`: Module for reading data from files.

7. **`main.py`**
   The main script of the project where the application starts. It initializes the bot, connects to the database, and launches the core components.

<hr>

# [Free AI Asistant v1.0.0a](https://t.me/FreeNeuroChat_bot "Telegram bot")(ru)
<hr>

## Description

Это телеграмм бот работающий через официальный *API DeepSeek, Qwen, Ozone, Mistral, microsoft*, а также доступен выбор других ИИ моделей.

Бот **полностью бесплатный**.


<hr>

## Install all dependencies and libs

```bash
cd pyconfig
uv sync --active
```
или
```bash
pip install -r pyconfig/requirements.txt
```

<hr>

## Projects Structure

1. **`configs`**
    _Эта директория содержит конфигурационные файлы проекта._

    * `__init__.py` : достает из .env параметры, инициализирует класс
    DataBase,     бота, диспетчера, создает HEADERS для запросов к API ИИ. Инициализирует такие публичные объекты, как:
        - bot
        - dp
        - DB
        - HEADERS
    * `.env` : Файл для хранения переменных окружения (например, токенов API,   настроек базы данных).
2. **`db`**
    _Директория, отвечающая за работу с базой данных._

    * `__init__.py` : Объединяет классы UserHistory и UserSettings в DataBase
    * `db_manager.py` : Основной модуль для управления базой данных     (подключение, отключение от БД). Является фундаментальным родителем для     остальных клсааов
    * `postgres_queries.py` : Содержит SQL-запросы для PostgreSQL.
    * `table_history.py` : Модуль для работы с таблицей истории запросов Юзера.
    * `table_usersettings.py` : Модуль для работы с таблицей пользовательских   настроек.
3. **`handlers`**
    _Директория, содержащая обработчики событий (для телеграмм Бота)._

    * `__init__.py` : Создает main_handler_router объект aiogram.Router, в котором содержаться все роутеры из модуля handlers
    * admin_handlers.py : Обработчики команд для администраторов: `/sendall`.
    * base_handlers.py : Базовые обработчики, `/start`, `/restart`, `/help`, `/info`
    * files_handler.py : Обработчики для работы с файлами.
    * history_handler.py : Обработчики для работы с историей запросов юзера: `/clear`.
    * messages_handlers.py : Обработчики для текстовых сообщений.
    * models_handlers.py : Обработчики, связанные с ИИ моделями: `/setmodel`, `/model`, `/setvisualmodel`, `/visualmodel` и callback queries.
    * photo_handlers.py : Обработчики для работы с фотографиями.
4. **`logs`**
    _Директория для хранения логов приложения._

    * `__init__.py` : Делает директорию logs пакетом Python.
    * `bot.log` : Файл логов для записи событий бота или приложения.
    * `events_logging.py` : Модуль для настройки и управления логированием событий: функция `setup_logger`
5. **`pyconfig`**
    _Директория для настройки среды разработки и управления зависимостями._

    * `.python-version` : Указывает версию Python, используемую в проекте.
    * `pyproject.toml` : Файл для настройки Poetry (менеджера пакетов) или других инструментов.
    * `requirements.txt` : Список зависимостей проекта.
    * `uv.lock` : Файл блокировки для менеджера пакетов uv (если используется).
6. **`utils`**
    _Директория с утилитарными функциями и вспомогательными модулями._

    * `__init__.py` : Делает директорию utils пакетом Python.
    * `ai_requests.py` : Модуль для асинхронных HTTP-запросов.
    * `correct_messages.py` : Модуль для корректировки или проверки сообщений.
    * `decorators.py` : Модуль для создания декораторов (для логирования или обработки ошибок).
    * `keyboard_utils.py` : Модуль для работы с клавиатурами (для Telegram-бота).
    * `messages.py`: Модуль для хранения шаблонов сообщений.
    * `read_files.py` : Модуль для чтения данных из файлов.
 
7. **`main.py`**
    *Главный скрипт* проекта, где происходит запуск приложения. Здесь подключается  бот, подключается база данных и запускаются основные компоненты.