from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from ..models import TelegramChats


async def get_group_chat(session, tg_chat_id):
    async with session() as session:
        async with session.begin():
            stmt = select(TelegramChats).where(TelegramChats.tg_chat_id == tg_chat_id)

            result = await session.execute(stmt)
            return result.scalars().one_or_none()


async def add_group_chat(session, group_chat_title, group_chat_id, group_chat_type):
    async with session() as session:
        async with session.begin():
            new_group_stmt = insert(TelegramChats).values(
                tg_chat_title=group_chat_title,
                tg_chat_id=group_chat_id,
                tg_chat_type=group_chat_type,
            )

            stmt = new_group_stmt.on_conflict_do_nothing(index_elements=["tg_chat_id"])
            await session.execute(stmt)
