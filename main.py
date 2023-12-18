import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from utils.stateforms import StepsForm

from handlers.command_handlers import (
    
    chat_member_update_handler,
    
    # Standart
    command_start_handler,
    command_help_handler,
    command_faq_handler,
    command_rules_handler,

    # # Group
    command_show_participants,
    command_participate_handler,
    command_all_mention_handler,
    command_activate_game,
    command_quit_game,
    # # Private
    command_cancel_event,
    command_edit_wish_list,
    command_notify_receiver,
)

from handlers.message_handler import (
    echo_handler,
    get_wish_title,
    get_wish_short_description,
    get_wish_link,

    message_add_wish_handler,
    message_delete_wish_handler,
)
from handlers.callback_handler import (
    participate_callback,
    not_participate_callback,
    delete_wish_callback,
    send_receiver_notification_callback,
    receiver_gift_ready_callback,
    gift_received_callback,
)

from aiogram.utils.chat_action import ChatActionMiddleware
from utils.callback_data import GroupInfo, WishInfo, ReceiverInfo,GiftReadyInfo,GiftReceivedInfo
from utils.commands import set_commands
from middlewares.bot_middlewares import CheckAdminMiddleware

from config import BOT_TOKEN, ADMIN_ID
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter
from aiogram.filters import IS_NOT_MEMBER, MEMBER
from db.db import setup_db


async def start_bot(bot: Bot):
    await set_commands(bot)
    await setup_db()
    await bot.send_message(ADMIN_ID, text="Бот Запущен")


async def shutdown_bot(bot: Bot):
    pass
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

    dp.my_chat_member.register(chat_member_update_handler,ChatMemberUpdatedFilter(IS_NOT_MEMBER >> MEMBER))
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
    dp.message.register(message_add_wish_handler, F.text == "Добавить Подарок", F.chat.type == "private")
    dp.message.register(message_delete_wish_handler, F.text == "Удалить Подарок", F.chat.type == "private")
    # dp.message.register(echo_handler)

    # FSM
    dp.message.register(get_wish_title, StepsForm.GET_wish_title)
    dp.message.register(
        get_wish_short_description, StepsForm.GET_wish_short_description
    )
    dp.message.register(get_wish_link, StepsForm.GET_wish_link)


    # Callbacks
    dp.callback_query.register(participate_callback, F.data == "participate")
    dp.callback_query.register(not_participate_callback, GroupInfo.filter())
    dp.callback_query.register(delete_wish_callback, WishInfo.filter())
    dp.callback_query.register(
        send_receiver_notification_callback, ReceiverInfo.filter()
    )
    dp.callback_query.register(receiver_gift_ready_callback,GiftReadyInfo.filter())
    dp.callback_query.register(gift_received_callback,GiftReceivedInfo.filter())

    # Bot Starts
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
