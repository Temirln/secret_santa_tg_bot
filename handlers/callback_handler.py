from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold

from db.crud.event import (
    get_chat_event,
    get_receiver_event,
    get_santa_chat_event,
    update_event_receiveer_giver,
)
from db.crud.participants import add_participant, delete_participant, get_participant
from db.crud.telegram_user import get_tg_user
from db.crud.wishlist import delete_user_wish, get_user_wishes, update_user_wish
from db.db import async_session_maker
from keyboards.inline_k import (
    create_inline_wish_buttons,
    get_inline_button_not_participate,
    get_inline_gift_list,
    get_inline_gift_received,
)
from keyboards.reply_k import get_reply_wish_list_markup
from utils.callback_data import (
    GiftReadyInfo,
    GiftReceivedInfo,
    GroupInfo,
    ReceiverInfo,
    WishInfo,
)
from utils.stateforms import StepsForm


async def participate_callback(call: CallbackQuery, bot: Bot):
    chat_id = call.message.chat.id

    if await get_chat_event(async_session_maker, chat_id):
        await bot.answer_callback_query(
            callback_query_id=call.id,
            text="Игра в этом чате уже начата, если хочешь принять участие, попроси администратора перезапустить игру или дождись новой игры",
            show_alert=True,
        )
        return

    user_tg_id = call.from_user.id
    firstname = call.from_user.first_name

    if not await get_tg_user(async_session_maker, user_tg_id):
        await bot.answer_callback_query(
            callback_query_id=call.id,
            text="Перед тем как нажать эту кнопку ты должен запустить бота по ссылке ниже или ввести в поиске \n@secret_santa_barbara_bot",
            show_alert=True,
        )
        return

    participant = await get_participant(async_session_maker, user_tg_id, chat_id)

    if participant:
        await bot.answer_callback_query(
            callback_query_id=call.id,
            text="Ты уже являешься участником",
            show_alert=False,
        )
    else:
        await add_participant(async_session_maker, firstname, user_tg_id, chat_id)
        await bot.answer_callback_query(
            callback_query_id=call.id,
            text="Ты теперь участвуешь в игре",
            show_alert=True,
        )

        group = await bot.get_chat(chat_id)
        await bot.send_message(
            user_tg_id,
            text=f"Поздравляю теперь ты участник Тайного Санты в группе {hbold(group.title)}\n\nЕсли ты случайно нажал или передумал участвовать можешь отказаться в любой момент нажав по кнопке ниже ",
            reply_markup=get_inline_button_not_participate(
                [tuple((chat_id, group.title))]
            ),
        )

        wishes = await get_user_wishes(async_session_maker, user_tg_id)

        if len(wishes) == 0:
            await bot.send_message(
                user_tg_id,
                text="""
Вашему Санте нужно знать, что вам дарить, опишите свой список желаний или пропустите этот шаг.

При желании, позже, вы сможете добавить или изменить свой список желаний.

Пока ты ждешь жеребьёвки, можешь добавить список подарков которые хотел бы получить. Через команду \n/update_wish_list
""",
                reply_markup=get_reply_wish_list_markup(),
            )


async def not_participate_callback(
    call: CallbackQuery, bot: Bot, callback_data: GroupInfo
):

    user_tg_id = call.from_user.id
    chat_id = callback_data.id

    group_chat = await bot.get_chat(chat_id)

    participant = await get_participant(async_session_maker, user_tg_id, chat_id)

    event = await get_santa_chat_event(async_session_maker, user_tg_id, chat_id)
    if event:
        await bot.answer_callback_query(
            callback_query_id=call.id,
            text=f"Ты не можешь отказаться от участия \nСанты уже распределены в группе {group_chat.title}\nЕсли ты передумал играть то сообщи Администратору группы и админ перезапустит игру для группы",
            show_alert=True,
        )
        return

    if participant:
        await delete_participant(async_session_maker, user_tg_id, chat_id)
        await bot.answer_callback_query(
            callback_query_id=call.id,
            text=f"Ты теперь не участник Тайного Санты группы {group_chat.title}",
            show_alert=True,
        )
        await call.message.delete()
    else:
        await bot.answer_callback_query(
            callback_query_id=call.id,
            text=f"Ты уже не являешься участником Тайного Санты группы {group_chat.title}",
            show_alert=False,
        )
        await call.message.delete()


async def delete_wish_callback(
    call: CallbackQuery, bot: Bot, callback_data: WishInfo, state: FSMContext
):
    wish_id = callback_data.id
    wish_title = callback_data.title

    await delete_user_wish(async_session_maker, wish_id)
    await bot.send_message(
        call.from_user.id, text=f"{wish_title} удален из вашего листа подарков"
    )
    await call.message.delete()
    await state.set_state(StepsForm.WISH_list_updated)

    events = await get_receiver_event(
        async_session_maker, receiver_id=call.from_user.id
    )
    print("Events:", len(events))

    wishes = await get_user_wishes(async_session_maker, call.from_user.id)
    if len(wishes) != 0:
        await bot.send_message(
            call.from_user.id,
            text="Мы оповестим Сант которые еще не подготовили свой подарок, что ты обновил(а) свой Список Желаний",
        )

        wishes_text = "Обновленный список желании\n"
        for index, wish in enumerate(wishes):
            wishes_text += (
                f"\n{index+1})\tНазвание : {wish.title}\n"
                f"{' ' * (4 if index+1 < 10 else 6)} Описание : {wish.description if wish.description else '—'}\n"
            )
    else:
        wishes_text = "Получатель очистил свой список желании"

    for event in events:
        if event.is_gift_ready:
            continue

        await bot.send_message(
            event.tg_santa_id, text="Ваш получатель обновил список желании"
        )

        await bot.send_message(
            event.tg_santa_id,
            text=wishes_text,
            parse_mode="html",
            reply_markup=create_inline_wish_buttons(wishes),
        )


async def send_receiver_notification_callback(
    call: CallbackQuery, callback_data: ReceiverInfo, bot: Bot
):
    receiver_id = callback_data.id
    chat = callback_data.chat
    giver_id = call.from_user.id

    await call.message.delete()

    wishes = await get_user_wishes(async_session_maker, receiver_id)
    if len(wishes) != 0:
        await call.message.answer(
            text="Выбери подарок который ты уже взял\nЯ лишь уведомлю получателя но не буду говорить какой подарок ты взял для него",
            reply_markup=get_inline_gift_list(chat, wishes),
        )
        # await call.message.delete()

    else:
        await call.message.answer(
            text="У получателя нет списка подарков но я его уведомил что ты взял подарок"
        )
        group_chat = await bot.get_chat(chat)
        msg = await bot.send_message(
            chat_id=receiver_id,
            text=f"Твой подарок из группы {group_chat.full_name} готов",
        )
        await bot.pin_chat_message(chat_id=receiver_id, message_id=msg.message_id)

    await update_event_receiveer_giver(async_session_maker, receiver_id, giver_id, chat)


async def receiver_gift_ready_callback(
    call: CallbackQuery, callback_data: GiftReadyInfo, bot: Bot
):
    chat = callback_data.chat
    receiver_id = callback_data.receiver
    wish_id = callback_data.id
    user_id = call.from_user.id

    await call.message.answer(text="Мы отправили сообщение твоему получателю")

    await call.message.delete()

    group_chat = await bot.get_chat(chat)
    msg = await bot.send_message(
        chat_id=receiver_id,
        text=f"Твой подарок из группы {group_chat.full_name} готов\nПосле того как получишь его можешь нажать на кнопку ниже и тем самым поблагодарить твоего Санту",
        reply_markup=get_inline_gift_received(wish_id, chat, user_id),
    )

    await bot.pin_chat_message(chat_id=receiver_id, message_id=msg.message_id)


async def gift_received_callback(
    call: CallbackQuery, callback_data: GiftReceivedInfo, bot: Bot
):
    wish_id = callback_data.wish
    await update_user_wish(async_session_maker, call.from_user.id, wish_id)

    await bot.answer_callback_query(
        callback_query_id=call.id, text="Мы отправили сообщение твоему Санте"
    )
    await call.message.delete()
    await bot.send_message(
        chat_id=callback_data.santa,
        text="Твой подарок был получен\nТеперь ты официально Санта",
    )
