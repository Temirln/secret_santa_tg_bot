from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    GET_wish_title = State()
    GET_wish_short_description = State()

    GET_wish_link = State()
    FINISH_wish = State()

    WISH_list_updated = State()
