import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import IS_NOT_MEMBER, MEMBER, Command
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter
from aiogram.utils.chat_action import ChatActionMiddleware

from config import ADMIN_ID, BOT_TOKEN
from db.db import setup_db
from handlers.callback_handler import (
    delete_wish_callback,
    gift_received_callback,
    not_participate_callback,
    participate_callback,
    receiver_gift_ready_callback,
    send_receiver_notification_callback,
)
from handlers.command_handlers import (  # Standart; # Group; # Private
    chat_member_update_handler,
    command_activate_game,
    command_all_mention_handler,
    command_cancel_event,
    command_edit_wish_list,
    command_faq_handler,
    command_help_handler,
    command_notify_receiver,
    command_participate_handler,
    command_quit_game,
    command_rules_handler,
    command_show_participants,
    command_start_handler,
)
from handlers.message_handler import (
    get_wish_link,
    get_wish_short_description,
    get_wish_title,
    message_add_wish_handler,
    message_delete_wish_handler,
    # echo_handler,
    get_price_chat,
    get_description_chat,
)
from middlewares.bot_middlewares import CheckAdminMiddleware
from utils.callback_data import (
    GiftReadyInfo,
    GiftReceivedInfo,
    GroupInfo,
    ReceiverInfo,
    WishInfo,
)
from utils.commands import set_commands
from utils.stateforms import StepsForm


async def start_bot(bot: Bot):
    await set_commands(bot)
    await setup_db()
    await bot.send_message(ADMIN_ID, text="Бот Запущен")


async def shutdown_bot(bot: Bot):
    await bot.send_message(ADMIN_ID, text="Бот Остановлен")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(shutdown_bot)

    # Middleware
    dp.message.middleware.register(ChatActionMiddleware())
    dp.message.middleware.register(CheckAdminMiddleware())

    dp.my_chat_member.register(
        chat_member_update_handler, ChatMemberUpdatedFilter(IS_NOT_MEMBER >> MEMBER)
    )
    dp.my_chat_member.register(chat_member_update_handler)

    # Commands

    # Standart commands
    dp.message.register(command_start_handler, Command(commands=["start"]))
    dp.message.register(command_help_handler, Command(commands=["help"]))
    dp.message.register(command_faq_handler, Command(commands=["faq"]))
    dp.message.register(command_rules_handler, Command(commands=["rules"]))

    # Group commands
    dp.message.register(
        command_participate_handler, Command(commands=["add_participants"])
    )
    dp.message.register(
        command_show_participants, Command(commands=["show_participants"])
    )
    dp.message.register(command_activate_game, Command(commands=["lets_start_party"]))
    dp.message.register(command_quit_game, Command(commands=["restart_secret_santa"]))
    dp.message.register(command_all_mention_handler, Command(commands=["all"]))

    # Private commands
    dp.message.register(command_edit_wish_list, Command(commands=["update_wish_list"]))
    dp.message.register(command_notify_receiver, Command(commands=["notify_santa"]))
    dp.message.register(command_cancel_event, Command(commands=["cancel"]))

    # Messages
    dp.message.register(
        message_add_wish_handler,
        F.text == "Добавить Подарок 🎁",
        F.chat.type == "private",
    )
    dp.message.register(
        message_delete_wish_handler,
        F.text == "Удалить Подарок ❌",
        F.chat.type == "private",
    )
    # dp.message.register(echo_handler)

    # FSM
    dp.message.register(get_wish_title, StepsForm.GET_wish_title)
    dp.message.register(
        get_wish_short_description, StepsForm.GET_wish_short_description
    )
    dp.message.register(get_wish_link, StepsForm.GET_wish_link)

    dp.message.register(get_price_chat, StepsForm.GET_chat_gift_price)
    dp.message.register(get_description_chat, StepsForm.GET_additional_description_chat)

    # Callbacks
    dp.callback_query.register(participate_callback, F.data == "participate")
    dp.callback_query.register(not_participate_callback, GroupInfo.filter())
    dp.callback_query.register(delete_wish_callback, WishInfo.filter())
    dp.callback_query.register(
        send_receiver_notification_callback, ReceiverInfo.filter()
    )
    dp.callback_query.register(receiver_gift_ready_callback, GiftReadyInfo.filter())
    dp.callback_query.register(gift_received_callback, GiftReceivedInfo.filter())

    # Bot Starts
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
