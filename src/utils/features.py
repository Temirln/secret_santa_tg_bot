import random

from pyrogram import Client, enums

from ..config import API_HASH, API_ID, BOT_TOKEN


async def get_all_members(chat_id: int, emojis: list):
    async with Client("santa", API_ID, API_HASH, bot_token=BOT_TOKEN) as app:
        return "\t".join(
            [
                f"<a href='tg://user?id={member.user.id}'>{random.choice(emojis)}</a>"
                async for member in app.get_chat_members(chat_id)
                if not member.user.is_bot
            ]
        )
