from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message


class CheckAdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if event.chat.type != "private":
            if event.chat.type != "supergroup":
                await event.answer(
                    "Чтобы пользоваться командами бота нужно дать разрешение на чтение и отправку сообщении"
                )
                return

        return await handler(event, data)
