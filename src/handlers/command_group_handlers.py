from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from constants.constant_text import SANTA_EMOJIS
from db.crud.event import delete_group_events, get_chat_event
from db.crud.participants import delete_chat_participants, get_chat_participants
from db.crud.telegram_chat import add_group_chat, get_group_chat
from db.db import async_session_maker
from keyboards.inline_k import get_inline_button
from utils.decorators import check_admin, check_chat
from utils.features import get_all_members
from utils.stateforms import StepsForm

group_commands_router = Router(name=__name__)


@group_commands_router.message(Command(commands=["add_participants"]))
@check_chat
@check_admin
async def command_participate_handler(message: Message, bot: Bot, *args, **kwargs):
    group_chat = await get_group_chat(async_session_maker, message.chat.id)

    if not group_chat:
        await add_group_chat(
            async_session_maker,
            message.chat.title,
            message.chat.id,
            message.chat.type,
        )

    if await get_chat_event(async_session_maker, message.chat.id):
        await message.answer(
            text="Участники уже распределены\n Если хотите добавить новых участников перезапустите игру через команду \n/restart_secret_santa"
        )
        return

    msg = await message.answer(
        text=f"Привествую всех \nНажав на кнопку {hbold('Участвовать')}\nВы можете принять участие в Тайном Санте для этой группы",
        reply_markup=get_inline_button(),
    )
    try:
        await bot.pin_chat_message(message.chat.id, msg.message_id)
    except Exception as e:
        print("Cannot Pin Message:", e)


@group_commands_router.message(Command(commands=["show_participants"]))
@check_chat
async def command_show_participants(message: Message, bot: Bot, *args, **kwargs):
    participants = await get_chat_participants(async_session_maker, message.chat.id)

    users = [
        (await bot.get_chat_member(message.chat.id, participant.tg_user_id)).user
        for participant in participants
    ]
    participants_text = "Участники Тайного Санты 🎅🏻🎄\n\n"
    participants_text += (
        "\n".join(
            [
                f"{index+1}) {hbold(participant.first_name)}{' - @' + participant.username if participant.username else '' }"
                for index, participant in enumerate(users)
            ]
        )
        if len(participants) != 0
        else "Пока никого нет\nПрисоединяйтесь!!!"
    )

    await message.reply(text=participants_text)


@group_commands_router.message(Command(commands=["lets_start_party"]))
@check_chat
@check_admin
async def command_activate_game(
    message: Message, bot: Bot, state: FSMContext, *args, **kwargs
):
    event = await get_chat_event(async_session_maker, message.chat.id)
    # chat_id = message.chat.id
    if event:
        await message.reply(
            text="Участники уже распределены\nЕсли хотите заново начать игру завершите предыдущую командой \n/restart_secret_santa"
        )
        return

    users = await get_chat_participants(async_session_maker, message.chat.id)
    if len(users) < 2:
        await message.answer(
            text="Слишком мало участников для игры, должно быть хотя бы 3 участника"
        )
        return

    await message.answer(
        text="""
Необходимо указать бюджет, сколько максимально должен стоить подарок?

Например: 5 000₸, 10 000₸ или $10  

(Если нажали случайно можете остановить командой /cancel)
"""
    )
    await state.set_state(StepsForm.GET_chat_gift_price)


@group_commands_router.message(Command(commands=["restart_secret_santa"]))
@check_chat
@check_admin
async def command_quit_game(message: Message, *args, **kwargs):
    chat_id = message.chat.id

    await delete_group_events(async_session_maker, chat_id)
    await delete_chat_participants(async_session_maker, chat_id)

    await message.reply(
        text="Все настройки для вашей группы сброшены\nВы можете начать игру сначала"
    )


@group_commands_router.message(Command(commands=["all"]))
@check_chat
async def command_all_mention_handler(message: Message, *args, **kwargs):
    members = await get_all_members(message.chat.id, SANTA_EMOJIS)
    all_mention = "Общий Сбор Сант \n\n" + members + "\n\nВроде всех позвал\nОбращайся😉"

    await message.answer(text=all_mention)
    await message.reply_sticker(
        sticker="CAACAgIAAxkBAAJoQGV9xcZjemruhcM6vVWLlgKFkAHGAAK3IwACrLwISQPq4WDxvT9TMwQ"
    )
