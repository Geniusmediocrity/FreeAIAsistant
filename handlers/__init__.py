from aiogram import Router

from .base_handlers import base_router
from .models_handlers import models_router
from .history_hadlers import hist_router
from .admin_handlers import admin_router
from .messages_handlers import messages_router
from .photo_handlers import photo_router
from .files_hadler import files_router


main_handler_router = Router(name=__name__)
main_handler_router.include_routers(
    base_router,
    models_router,
    hist_router,
    admin_router,
    messages_router,
    files_router,
    photo_router
)   