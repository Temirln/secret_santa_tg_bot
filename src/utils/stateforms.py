from aiogram.fsm.state import State, StatesGroup


class StepsForm(StatesGroup):
    GET_wish_title = State()
    GET_wish_short_description = State()

    GET_wish_link = State()
    FINISH_wish = State()

    WISH_list_updated = State()

    GET_chat_gift_price = State()
    GET_additional_description_chat = State()
