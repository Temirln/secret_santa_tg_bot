from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from ..constants.constant_text import (
    EMOJIS,
    FAQ_TEXT,
    HELP_TEXT,
    RULES_TEXT,
    START_TEXT_GROUP,
    START_TEXT_PRIVATE,
)
from ..db.crud.telegram_chat import add_group_chat, get_group_chat
from ..db.crud.telegram_user import add_tg_user, get_tg_user
from ..db.db import async_session_maker
from ..utils.features import get_all_members

standart_commands_router = Router(name=__name__)


@standart_commands_router.message(Command(commands=["start"]))
async def command_start_handler(message: Message) -> None:
    if message.chat.type == "supergroup":
        group_chat = await get_group_chat(async_session_maker, message.chat.id)

        if not group_chat:
            await add_group_chat(
                async_session_maker,
                message.chat.title,
                message.chat.id,
                message.chat.type,
            )

        members = await get_all_members(message.chat.id, EMOJIS)

        await message.answer(
            text=START_TEXT_GROUP.format(group_name=hbold(message.chat.title)) + members
        )

    elif message.chat.type == "private":
        if not await get_tg_user(async_session_maker, message.from_user.id):
            await add_tg_user(
                async_session_maker,
                message.from_user.id,
                message.from_user.username,
                message.from_user.full_name,
            )

        await message.answer(
            START_TEXT_PRIVATE.format(user_name=hbold(message.from_user.full_name))
        )


@standart_commands_router.message(Command(commands=["help"]))
async def command_help_handler(message: Message):
    await message.answer(text=HELP_TEXT)


@standart_commands_router.message(Command(commands=["rules"]))
async def command_rules_handler(message: Message):
    await message.answer(text=RULES_TEXT)


@standart_commands_router.message(Command(commands=["faq"]))
async def command_faq_handler(message: Message):
    await message.answer(text=FAQ_TEXT)
