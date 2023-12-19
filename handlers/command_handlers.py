from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ChatMemberUpdated, Message, ReplyKeyboardRemove
from aiogram.utils.markdown import hbold

from constants.constant_text import (
    FAQ_TEXT,
    HELP_TEXT,
    RULES_TEXT,
    START_TEXT_GROUP,
    START_TEXT_PRIVATE,
    emojis,
    santa_emojis,
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


async def command_start_handler(message: Message) -> None:
    if message.chat.type == "supergroup":

        members = await get_all_members(message.chat.id, emojis)

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

            await update.answer("Бот Тайна Санта готов к работе")
        elif update.new_chat_member.status == "member" and update.chat.type == "group":
            await update.answer(
                f"<a href='tg://user?id={update.from_user.id}'>{update.from_user.full_name}</a>, Привет! Я помогу вам в игре Тайный Санта. Для продолжения выдайте мне права и разрешение читать и отправлять сообщения в настройках группы"
            )

        elif update.new_chat_member.status == "left":
            await delete_group_events(async_session_maker, update.chat.id)
            await delete_chat_participants(async_session_maker, update.chat.id)


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


@check_private
async def command_notify_receiver(message: Message, bot: Bot, *args, **kwargs):
    santa_event = await get_santa_event(async_session_maker, message.from_user.id)
    receivers = [
        (receiver.tg_receiver_id, receiver.tg_chat_id)
        for receiver in santa_event
        if not receiver.is_gift_ready
    ]

    if len(receivers) > 0:
        await message.answer(
            text="Выбери получателя которого хочешь оповестить",
            reply_markup=await get_inline_receivers(receivers),
        )
    else:
        if len(santa_event) == 0:
            await message.answer(text="У тебя пока нет получателей")
        else:
            await message.answer(
                text="Ты уже подготовил подарки для своих получателей, Молодец"
            )


async def command_edit_wish_list(message: Message, state: FSMContext, *args, **kwargs):
    wishes = await get_user_wishes(async_session_maker, message.from_user.id)

    wishes_text = "Ваш список желаний ⬇️\n"
    if len(wishes) != 0:
        for index, wish in enumerate(wishes):
            wishes_text += (
                f"\n{index+1}) \tНазвание : {wish.title}\n"
                f"{' ' * (4 if index+1 < 10 else 6)}\tОписание : {wish.description if wish.description else '—'}\n"
            )
    else:
        wishes_text += "\nЗдесь пока пусто😕"

    await message.answer(
        text=wishes_text, reply_markup=create_inline_wish_buttons(wishes)
    )

    await message.answer(
        text="Ты можешь дополнить или убрать желание из списка",
        reply_markup=get_reply_wish_list_markup(),
    )


async def command_help_handler(message: Message):
    await message.answer(text=HELP_TEXT)


async def command_faq_handler(message: Message):
    await message.answer(text=FAQ_TEXT)


async def command_rules_handler(message: Message):
    await message.answer(text=RULES_TEXT)


@check_chat
@check_admin
async def command_participate_handler(message: Message, bot: Bot, *args, **kwargs):

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


@check_chat
@check_admin
async def command_quit_game(message: Message, *args, **kwargs):
    chat_id = message.chat.id

    await delete_group_events(async_session_maker, chat_id)
    await delete_chat_participants(async_session_maker, chat_id)

    await message.reply(
        text="Все настройки для вашей группы сброшены\nВы можете начать игру сначала"
    )


@check_chat
async def command_all_mention_handler(message: Message, *args, **kwargs):

    members = await get_all_members(message.chat.id, santa_emojis)
    all_mention = "Общий Сбор Сант \n\n" + members + "\n\nВроде всех позвал\nОбращайся😉"

    await message.answer(text=all_mention)
    await message.reply_sticker(
        sticker="CAACAgIAAxkBAAJoQGV9xcZjemruhcM6vVWLlgKFkAHGAAK3IwACrLwISQPq4WDxvT9TMwQ"
    )


@check_private
async def command_cancel_event(message: Message, state: FSMContext, *args, **kwargs):
    await state.clear()
    await message.reply(
        text="Текущее действие прервано", reply_markup=ReplyKeyboardRemove()
    )


@check_chat
@check_admin
async def command_activate_game(message: Message, bot: Bot, *args, **kwargs):
    event = await get_chat_event(async_session_maker, message.chat.id)
    chat_id = message.chat.id
    if event:
        await message.reply(
            text="Участники уже распределены\nЕсли хотите заново начать игру завершите предыдущую командой \n/restart_secret_santa"
        )
        return

    users = await get_chat_participants(async_session_maker, message.chat.id)

    usernames = [
        (await bot.get_chat_member(message.chat.id, participant.tg_user_id)).user
        for participant in users
    ]
    usernames_text = "\n".join(
        [
            f"{hbold(participant.first_name)}{' - @' + participant.username if participant.username else '' }"
            for participant in usernames
        ]
    )
    if len(users) < 1:
        await message.answer(
            text="Слишком мало участников для игры, должно быть хотя бы 3 участника"
        )
        return

    await message.reply_animation(
        animation="CgACAgIAAx0CejIa0QADnWV95EmYSBdb_qBdc4D9z-KKw5x6AAJuKQAChzHQS9nN24bhArx5MwQ",
        caption=f"Начинаем распределение участников\n\n{usernames_text}\n\nВсем в личные сообщения были высланы имена и аккаунты ваших Получателей\n\nВеселой всем игры",
    )

    shuffle_users = arrange_secret_santa(users)

    for giver, receiver in shuffle_users.items():
        tg_user = (await bot.get_chat_member(chat_id, receiver.tg_user_id)).user

        await bot.send_message(
            giver.tg_user_id,
            text=f"Привет Санта\nТвоим получателем будет \n\n<span class='tg-spoiler'>{hbold(tg_user.first_name)} {'@'+tg_user.username if tg_user.username else ''}</span>",
            parse_mode="html",
        )
        wishes = await get_user_wishes(async_session_maker, receiver.tg_user_id)
        if len(wishes) != 0:
            wishes_text = "Это список того что вы можете подарить своему получателю\n"
            for index, wish in enumerate(wishes):
                if wish.is_gift_received:
                    continue

                wishes_text += f"""
{index+1})\tНазвание: {wish.title}
\t\t\t\t\tОписание: {wish.description}
"""
            await bot.send_message(
                giver.tg_user_id,
                text=wishes_text,
                reply_markup=create_inline_wish_buttons(wishes),
            )
        else:
            # user = await bot.get_chat_member(message.chat.id,receiver.telegram_id)
            await bot.send_message(
                receiver.tg_user_id,
                text=f"Ты не предоставил(а) список подарков который хотел(а) бы получить\nТвоему Тайному Санте будет труднее выбрать тебе подарок \nМожешь исправить это командой /update_wish_list",
            )
        await arrange_all_giver_receiver(
            async_session_maker,
            giver.tg_user_id,
            receiver.tg_user_id,
            message.chat.id,
        )
