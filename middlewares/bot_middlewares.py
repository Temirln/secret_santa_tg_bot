from typing import Dict, Any, Callable, Awaitable
from aiogram import BaseMiddleware 
from aiogram.types import Message
from db.crud.telegram_chat import get_group_chat,add_group_chat
from db.db import async_session_maker
from utils.features import get_all_members
import random
from constants.constant_text import start_text_group
from aiogram.utils.markdown import hbold
from aiogram.exceptions import TelegramMigrateToChat
from aiogram.client.session.middlewares.base import (
    Response,
    TelegramMethod,
    TelegramType,
    BaseRequestMiddleware, 
    NextRequestMiddlewareType
)

class CheckAdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        
        
        # await event.answer("Middleware")
        if event.chat.type != "private":
            if event.chat.type != "supergroup":            
                await event.answer("Чтобы пользоваться командами бота нужно дать разрешение на чтение и отправку сообщении")
                return 


        print("EVENT:",event)
        
        return await handler(event, data)

        