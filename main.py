import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.utils.chat_action import ChatActionMiddleware

from config import ADMIN_ID, BASE_WEBHOOK_URL, BOT_TOKEN, WEBHOOK_PATH, WEBHOOK_SECRET
from db.db import setup_db
from handlers.action_handlers import actions_router
from handlers.callback_handler import callbacks_router
from handlers.command_group_handlers import group_commands_router
from handlers.command_private_handlers import private_commands_router
from handlers.command_standart_handlers import standart_commands_router
from handlers.message_handler import messages_router
from handlers.state_handlers import states_router
from middlewares.bot_middlewares import CheckAdminMiddleware
from utils.commands import set_commands


async def start_bot(bot: Bot):
    await set_commands(bot)
    await setup_db()
    await bot.set_webhook(
        f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET
    )
    await bot.send_message(ADMIN_ID, text="Бот Запущен")


async def shutdown_bot(bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.send_message(ADMIN_ID, text="Бот Остановлен")


async def main() -> None:
    # def main():
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(shutdown_bot)

    # Middleware
    dp.message.middleware.register(ChatActionMiddleware())
    dp.message.middleware.register(CheckAdminMiddleware())

    dp.include_router(standart_commands_router)
    dp.include_router(group_commands_router)
    dp.include_router(messages_router)
    dp.include_router(private_commands_router)
    dp.include_router(states_router)
    dp.include_router(callbacks_router)
    dp.include_router(actions_router)

    # Bot Starts
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

    # Webhook
    # app = web.Application()
    # webhook_requests_handler = SimpleRequestHandler(
    #     dispatcher=dp,
    #     bot=bot,
    #     secret_token=WEBHOOK_SECRET,
    # )
    # webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    # setup_application(app, dp, bot=bot)
    # web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

    # main()
