from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from db.crud.wishlist import get_user_wishes
from db.db import async_session_maker
from keyboards.inline_k import get_inline_wishes_list
from utils.decorators import check_private
from utils.stateforms import StepsForm

messages_router = Router(name=__name__)


@messages_router.message(F.text == "Добавить Подарок 🎁", F.chat.type == "private")
@check_private
async def message_add_wish_handler(
    message: Message, state: FSMContext, *args, **kwargs
):
    await message.answer(
        text="🎁Начинаем сбор информации о подарке🎁\n\nЕсли запустил действие случайно то можешь отменить командой \n/cancel\n\n\nВведи название подарка который хочешь получить:"
    )
    await state.set_state(StepsForm.GET_wish_title)


@messages_router.message(F.text == "Удалить Подарок ❌", F.chat.type == "private")
@check_private
async def message_delete_wish_handler(message: Message, *args, **kwargs):
    gifts = await get_user_wishes(async_session_maker, message.from_user.id)
    if len(gifts) == 0:
        await message.answer("Твой Список Желаний Пуст")
        return

    await message.answer(
        text="Выбери какой подарок из списка который хочешь удалить",
        reply_markup=get_inline_wishes_list(gifts),
    )


@messages_router.message()
async def echo_handler(message: Message, bot: Bot) -> None:
    print("GIF:", message.animation)
    print("GROUP:", message.chat.type)
    print("GROUP_ID:", message.chat.id)

    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")
