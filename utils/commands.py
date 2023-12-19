from aiogram import Bot
from aiogram.types import (
    BotCommand,
    BotCommandScopeAllChatAdministrators,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
)


async def set_commands(bot: Bot):

    standart_commands = [
        BotCommand(command="start", description="Запуск бота"),
        BotCommand(command="help", description="Список всех комманд"),
        BotCommand(command="faq", description="Часто Задаваемые Вопросы"),
        BotCommand(command="rules", description="Правила игры в Тайного Санту"),
    ]

    group_commands = [
        BotCommand(command="all", description="Упомянуть Всех "),
        BotCommand(
            command="show_participants", description="Показать Список всех Участников"
        ),
    ]

    group_administratot_commands = [
        BotCommand(command="add_participants", description="Кнопка участия в игре"),
        BotCommand(
            command="lets_start_party", description="Начать Жеребьёвку Участников"
        ),
        BotCommand(command="restart_secret_santa", description="Остановить Игру"),
    ]

    private_commands = [
        BotCommand(command="update_wish_list", description="Обновить Список Желаний"),
        BotCommand(
            command="notify_santa",
            description="Оповестить своего получателя о готовом подарке",
        ),
        # BotCommand(
        #     command="all_chats",
        #     description="Список всех чатов где участвую в ",
        # ),
    ]

    await bot.set_my_commands(
        standart_commands + private_commands, scope=BotCommandScopeAllPrivateChats()
    )
    await bot.set_my_commands(
        standart_commands + group_commands, scope=BotCommandScopeAllGroupChats()
    )
    await bot.set_my_commands(
        standart_commands + group_commands + group_administratot_commands,
        scope=BotCommandScopeAllChatAdministrators(),
    )
