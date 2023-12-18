# from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.callback_data import GroupInfo, WishInfo, ReceiverInfo,GiftReadyInfo,GiftReceivedInfo
from db.crud.participants import get_participant
from db.db import async_session_maker


def create_inline_wish_buttons(wishes):
    keyboard_builder = InlineKeyboardBuilder()
    for wish in wishes:
        if wish.link:
            keyboard_builder.button(text=f"Ссылка на {wish.title}", url=wish.link)
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()



from  aiogram.types.switch_inline_query_chosen_chat import SwitchInlineQueryChosenChat
def get_inline_button():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="⛄️Участвовать☃️", 
        callback_data="participate",
    )
    keyboard_builder.button(
        text="Перейти в Бота 🤖", 
        url = "t.me/picturebook_bot",
    )

    keyboard_builder.adjust(1)

    return keyboard_builder.as_markup()


def get_inline_button_not_participate(groups: list[(int,str)]):

    keyboard_builder = InlineKeyboardBuilder()
    for id, title in groups:
        # group = await bot.get_chat(g)
        # print(group)
        keyboard_builder.button(
            text=f"Отказаться {title}", callback_data=GroupInfo(id=id)
        )

    return keyboard_builder.as_markup()


def get_inline_wishes_list(wishes):
    keyboard_builder = InlineKeyboardBuilder()
    for wish in wishes:
        keyboard_builder.button(
            text=f"{wish.title}", callback_data=WishInfo(id=wish.id, title=wish.title)
        )
    
    keyboard_builder.adjust(1)

    return keyboard_builder.as_markup()

def get_inline_gift_list(chat_id,wishes):
    keyboard_builder = InlineKeyboardBuilder()
    for wish in wishes:
        if wish.is_gift_received:
            continue 

        keyboard_builder.button(
            text=f"{wish.title}", callback_data=GiftReadyInfo(id=wish.id, title=wish.title,chat = chat_id, receiver = wish.tg_user_id)
        )

    keyboard_builder.adjust(1)

    return keyboard_builder.as_markup()


async def get_inline_receivers(receivers):
    keyboard_builder = InlineKeyboardBuilder()
    for receiver_id, receiver_chat in receivers:
        receiver = await get_participant(
            async_session_maker, receiver_id, receiver_chat
        )

        keyboard_builder.button(
            text=f"{receiver.tg_user_firstname}",
            callback_data=ReceiverInfo(id=receiver.tg_user_id, chat=receiver_chat),
        )
    


    return keyboard_builder.as_markup()


def get_inline_gift_received(wish_id,chat_id,santa_id):
    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.button(
        text=f"Подарок получен🥰",
        callback_data=GiftReceivedInfo(wish = wish_id,chat=chat_id, santa= santa_id),
    )
    return keyboard_builder.as_markup()