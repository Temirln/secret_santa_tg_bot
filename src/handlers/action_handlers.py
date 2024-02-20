from aiogram import Bot, Router
from aiogram.types import ChatMemberUpdated
from aiogram.utils.markdown import hbold

from ..constants.constant_text import EMOJIS, START_TEXT_GROUP
from ..db.crud.event import delete_group_events
from ..db.crud.participants import delete_chat_participants
from ..db.crud.telegram_chat import add_group_chat, get_group_chat
from ..db.db import async_session_maker
from ..utils.features import get_all_members

actions_router = Router()


@actions_router.my_chat_member()
async def chat_member_update_handler(update: ChatMemberUpdated, bot: Bot):
    print("UPDATE:", update.new_chat_member)

    if update.new_chat_member.user.id == bot.id:
        if (
            update.new_chat_member.status == "member"
            and update.chat.type == "supergroup"
        ):
            group_chat = await get_group_chat(async_session_maker, update.chat.id)

            if not group_chat:
                await add_group_chat(
                    async_session_maker,
                    update.chat.title,
                    update.chat.id,
                    update.chat.type,
                )

            members = await get_all_members(update.chat.id, EMOJIS)

            await update.answer(
                text=START_TEXT_GROUP.format(group_name=hbold(update.chat.title))
                + members
            )
        elif update.new_chat_member.status == "member" and update.chat.type == "group":
            await update.answer(
                f"<a href='tg://user?id={update.from_user.id}'>{update.from_user.full_name}</a>, Привет! Я помогу вам в игре Тайный Санта. Для продолжения выдайте мне права админа и разрешение читать и отправлять сообщения в настройках группы"
            )

        elif update.new_chat_member.status == "left":
            await delete_group_events(async_session_maker, update.chat.id)
            await delete_chat_participants(async_session_maker, update.chat.id)
