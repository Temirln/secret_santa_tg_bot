from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_reply_wish_next_step_markup():
    reply_builder = ReplyKeyboardBuilder()

    reply_builder.button(text="Пропустить Действие")
    reply_builder.adjust(1)

    return reply_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Можешь пропустить этот шаг",
    )

def get_reply_wish_list_markup():
    reply_builder = ReplyKeyboardBuilder()

    reply_builder.button(text="Добавить Подарок")
    reply_builder.button(text="Удалить Подарок")
    reply_builder.adjust(1)

    return reply_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выбери Действие ⬇️",
    )
