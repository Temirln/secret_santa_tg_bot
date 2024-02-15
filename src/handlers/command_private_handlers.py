from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.markdown import hbold

from db.crud.event import get_santa_event
from db.crud.wishlist import get_user_wishes
from db.db import async_session_maker
from keyboards.inline_k import create_inline_wish_buttons, get_inline_receivers
from keyboards.reply_k import get_reply_wish_list_markup
from utils.decorators import check_private

private_commands_router = Router(name=__name__)


@private_commands_router.message(Command(commands=["update_wish_list"]))
async def command_edit_wish_list(message: Message, state: FSMContext, *args, **kwargs):
    wishes = await get_user_wishes(async_session_maker, message.from_user.id)

    wishes_text = "Ваш список желаний ⬇️\n"
    if len(wishes) != 0:
        for index, wish in enumerate(wishes):
            wishes_text += (
                f"\n{index+1}) \t{hbold('Название')} : {wish.title}\n"
                f"{' ' * (4 if index+1 < 10 else 6)}\t{hbold('Описание')} : {wish.description if wish.description else '—'}\n"
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


@private_commands_router.message(Command(commands=["notify_santa"]))
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


@private_commands_router.message(Command(commands=["cancel"]))
# @check_private
async def command_cancel_event(message: Message, state: FSMContext, *args, **kwargs):
    await state.clear()
    await message.reply(
        text="Текущее действие прервано", reply_markup=ReplyKeyboardRemove()
    )
