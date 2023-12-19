from aiogram import Bot
from aiogram.types import Message


def check_private(func):
    async def wrapper(message: Message, *args, **kwargs):
        if message.chat.type == "private":
            return await func(message, *args, **kwargs)
        await message.reply(text="Это команда работает только в личном сообщении бота")

    return wrapper


def check_private_messages(func):
    async def wrapper(message: Message, *args, **kwargs):
        if message.chat.type == "private":
            return await func(message, *args, **kwargs)
        return await func(message, *args, **kwargs)
        # await message.reply(text = "Это команда работает только в личном сообщении бота")

    return wrapper


def check_chat(func):
    async def wrapper(message: Message, *args, **kwargs):
        if message.chat.type in ["group", "supergroup"]:
            return await func(message, *args, **kwargs)
        await message.reply(text="Это команда работает только в Группах")

    return wrapper


def check_admin(func):
    async def wrapper(message: Message, bot: Bot, *args, **kwargs):
        user = await bot.get_chat_member(message.chat.id, message.from_user.id)
        if user.status.value in ["administrator", "creator"]:
            return await func(message, bot, *args, **kwargs)

        await message.reply_animation(
            # animation="CgACAgIAAxkBAAINeGV94qwIlxu8EY6o-sZz0as3AAGmjgAC_kIAAq7n8Eu1om4yExzheDME",
            animation="CgACAgIAAxkBAAMpZYEcq_9hS90vJn_DZ8aBx95A-6sAAv5CAAKu5_BLZ3yxbbi6QXozBA",
            caption="Эта команда не доступна для тех, кто плохо вел себя в этом году",
        )

    return wrapper
