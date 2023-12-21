from aiogram.filters.callback_data import CallbackData


class GroupInfo(CallbackData, prefix="group_id"):
    id: int


class WishInfo(CallbackData, prefix="wish_id"):
    id: int
    title: str


class GiftReadyInfo(CallbackData, prefix="wish_id"):
    id: int
    chat: int
    receiver: int


class GiftReceivedInfo(CallbackData, prefix="gift_id"):
    wish: int
    chat: int
    santa: int


class ReceiverInfo(CallbackData, prefix="receiver_id"):
    id: int
    chat: int


class ReceiverInfo(CallbackData, prefix="receiver_id"):
    id: int
    chat: int
