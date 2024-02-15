from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import ChatMemberUpdated, Message, ReplyKeyboardRemove
from aiogram.utils.markdown import hbold

from constants.constant_text import (
    EMOJIS,
    FAQ_TEXT,
    HELP_TEXT,
    RULES_TEXT,
    SANTA_EMOJIS,
    START_TEXT_GROUP,
    START_TEXT_PRIVATE,
)
from db.crud.event import (
    arrange_all_giver_receiver,
    delete_group_events,
    get_chat_event,
    get_santa_event,
)
from db.crud.participants import delete_chat_participants, get_chat_participants
from db.crud.telegram_chat import add_group_chat, get_group_chat
from db.crud.telegram_user import add_tg_user, get_tg_user
from db.crud.wishlist import get_user_wishes
from db.db import async_session_maker
from keyboards.inline_k import (
    create_inline_wish_buttons,
    get_inline_button,
    get_inline_receivers,
)
from keyboards.reply_k import get_reply_wish_list_markup
from utils.decorators import check_admin, check_chat, check_private
from utils.features import get_all_members
from utils.shuffle_user import arrange_secret_santa
from utils.stateforms import StepsForm

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
