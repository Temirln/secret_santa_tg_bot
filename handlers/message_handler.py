"""
Created By: Temirlan
"""

import re

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hcode, hlink,hitalic

from db.crud.event import get_receiver_event, arrange_all_giver_receiver
from db.crud.wishlist import add_user_wish, get_user_wishes
from db.crud.participants import get_chat_participants
from db.db import async_session_maker
from keyboards.inline_k import create_inline_wish_buttons, get_inline_wishes_list
from keyboards.reply_k import (
    get_reply_wish_list_markup,
    get_reply_wish_next_step_markup,
)
from utils.decorators import check_private
from utils.stateforms import StepsForm
from utils.shuffle_user import arrange_secret_santa 


async def echo_handler(message: Message, bot: Bot) -> None:
    print("GIF:",message.animation)
    print("GROUP:", message.chat.type)
    print("GROUP_ID:", message.chat.id)

    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


@check_private
async def get_wish_title(message: Message, state: FSMContext, *args, **kwargs):
    if message.text.title().strip() == "Пропустить Действие ⏭":
        await message.answer(text="Название подарка обязательна")
        return

    await state.update_data(title=message.text)
    await state.set_state(StepsForm.GET_wish_short_description)
    await message.answer(
        text=f"Теперь можешь ввести короткое описание для твоего подарка\n\nГде его можно найти или как он должен выглядеть.\nК примеру: \n\n{hcode('Я хочу получить от Тайного Санты стеклянный снежный шар с елкой внутри и ...')}",
        reply_markup=get_reply_wish_next_step_markup(),
    )


@check_private
async def get_wish_short_description(
    message: Message, state: FSMContext, *args, **kwargs
):
    if message.text.strip().title() != "Пропустить Действие ⏭":
        await state.update_data(desc=message.text)

    await state.set_state(StepsForm.GET_wish_link)
    await message.answer(
        text=f"Если это вещь с интернета можешь скинуть {hbold('Cсылку')} на подарок чтобы твой Cанта взял его тебе или посмотрел как подарок должен выглядеть:"
    )


@check_private
async def get_wish_link(message: Message, bot: Bot, state: FSMContext, *args, **kwargs):
    if message.text.strip().title() != "Пропустить Действие ⏭":
        # state.set_state(StepsForm.FINISH_wish)
        url_pattern = re.compile(
            r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
        )
        wish_link = message.text
        print(url_pattern.search(wish_link))
        if not url_pattern.search(wish_link):
            await message.reply(text="Ты прислал не ссылку")
            return

        await state.update_data(link=wish_link)

    context_data = await state.get_data()
    title = context_data.get("title")
    desc = context_data.get("desc")
    link = context_data.get("link")
    wish_data = {"title": title, "desc": desc, "link": link}

    await add_user_wish(async_session_maker, message.from_user.id, wish_data)

    wish_data = (
        f"Я записал данные твоего подарка\r\n\n"
        f"Название: {hbold(title)}\n"
        f'Описание: {desc if desc else "—"}\n\n'
        f'Ссылка: {hlink(title="Подарок",url=link) if link else "—"}\n'
    )

    event = await get_receiver_event(async_session_maker, message.from_user.id)
    if event:
        wishes = await get_user_wishes(async_session_maker, message.from_user.id)
        wishes_text = "Это список того что вы можете подарить своему получателю"
        for index, wish in enumerate(wishes):
            if wish.is_gift_received:
                continue

            wishes_text += (
                f"\n{index+1})\tНазвание  : {wish.title}\n"
                f"{' ' * (4 if index+1 < 10 else 6)}Описание : {wish.description if wish.description else '—'}\n"
            )
        for e in event:
            if e.is_gift_ready:
                continue

            await bot.send_message(
                e.tg_santa_id, text="Ваш получатель обновил список подарков"
            )
            await bot.send_message(
                e.tg_santa_id,
                text=wishes_text,
                parse_mode="html",
                reply_markup=create_inline_wish_buttons(wishes),
            )
        await message.answer(
            text="Я оповестил твоих Сант которые еще не подготовили тебе подарок что ты обновил список подарков"
        )
    else:
        await message.answer(
            text="Все отлично когда будет распределение участников твой Лист Желаний будет виден твоему Тайному Санте"
        )

    await message.answer(
        text=wish_data,
        disable_web_page_preview=True,
        reply_markup=get_reply_wish_list_markup(),
    )
    await state.clear()


@check_private
async def message_add_wish_handler(
    message: Message, state: FSMContext, *args, **kwargs
):
    await message.answer(
        text="🎁Начинаем сбор информации о подарке🎁\n\nЕсли запустил действие случайно то можешь отменить действие командой \n/cancel\n\n\nВведи название подарка который хочешь получить:"
    )
    await state.set_state(StepsForm.GET_wish_title)


# @check_private
async def message_delete_wish_handler(message: Message, *args, **kwargs):
    gifts = await get_user_wishes(async_session_maker, message.from_user.id)
    if len(gifts) == 0:
        await message.answer("Твой Список Желаний Пуст")
        return

    await message.answer(
        text="Выбери какой подарок из списка который хочешь удалить",
        reply_markup=get_inline_wishes_list(gifts),
    )


async def get_price_chat(message: Message, bot: Bot, state: FSMContext):

    await state.update_data(price = message.text)
    await message.answer(text = """
Напишите правило: день, место или каким образом будет передаваться подарки. Можете тут же добавить дополнительную информацию. Что можно, а что нельзя дарить. И прочие детали игры.

(Если нажали случайно можете остановить командой /cancel)
"""
    )
    await state.set_state(StepsForm.GET_additional_description_chat)


async def get_description_chat(message: Message, bot: Bot, state: FSMContext):
    organizer = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    await state.update_data(desc=message.text)

    context_data = await state.get_data()
    price = context_data.get("price")
    desc = context_data.get("desc")

    await state.clear()


    chat_id = message.chat.id
    users = await get_chat_participants(async_session_maker, message.chat.id)

    usernames = [
        (await bot.get_chat_member(message.chat.id, participant.tg_user_id)).user
        for participant in users
    ]
    usernames_text = "\n".join(
        [
            f"<a href='tg://user?id={participant.id}'>{hbold(participant.first_name)}</a>"
            for participant in usernames
        ]
    )
    

    await message.reply_animation(
        animation="CgACAgIAAxkBAAMuZYEeFYJputUAAVSbkP30lPZANsAhAAJuKQAChzHQS600eUKFozYHMwQ",
        caption=f"Начинаем распределение участников\n\n{hbold('Организатор')}: {organizer}\n{hbold('Бюджет:')} {price}\n{hbold('Правила Группы:')} {hitalic(desc)}\n\n{hbold('Учатсники:')}\n{usernames_text}\n\nВсем в личные сообщения были высланы имена и аккаунты ваших Получателей\n\nВеселой всем игры",
    )

    shuffle_users = arrange_secret_santa(users)

    for giver, receiver in shuffle_users.items():
        tg_user = (await bot.get_chat_member(chat_id, receiver.tg_user_id)).user

        msg = await bot.send_message(
            giver.tg_user_id,
            text=f"""
Привет Санта\nТвоим получателем будет \n\n<span class='tg-spoiler'>{hbold(tg_user.first_name)} {'@'+tg_user.username if tg_user.username else ''}</span>

{hbold('Организатор')}: {organizer}
{hbold('Бюджет')}: {price}
{hbold('Правила группы:')} {desc if desc else "Отсутсвует"}
""",
            parse_mode="html",
        )

        await bot.pin_chat_message(chat_id = giver.tg_user_id, message_id=msg.message_id)

        wishes = await get_user_wishes(async_session_maker, receiver.tg_user_id)
        
        if len(wishes) != 0:
            wishes_text = f"Это список того что вы можете подарить <a href='tg://user?id={tg_user.id}'>{tg_user.first_name}</a>\n"
            index = 1
            for wish in wishes:
                if wish.is_gift_received:
                    continue
                
                wishes_text += f"""
{index})\tНазвание: {wish.title}
\t\t\t\t\tОписание: {wish.description}
"""
                index += 1
            if index == 1:
                await bot.send_message(
                    receiver.tg_user_id,
                    text=f"Добавь новые желания в свой список\nВсе старые ты уже получил"
                )
            else:
                await bot.send_message(
                    giver.tg_user_id,
                    text=wishes_text,
                    reply_markup=create_inline_wish_buttons(wishes),
                )
        else:
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