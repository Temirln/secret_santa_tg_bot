from ..models import TelegramUsers

# from .db import session,get_async_session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, delete, update
from db.models import TelegramUsers

async def get_tg_user(session, tg_user_id):
    async with session() as session:
        async with session.begin():
            stmt = select(TelegramUsers).where(
                TelegramUsers.tg_user_id == tg_user_id
            )

            result = await session.execute(stmt)
            return result.scalars().one_or_none()
        
async def add_tg_user(session, tg_user_id, tg_user_username, tg_user_fullname):
    async with session() as session:
        async with session.begin():
            stmt = insert(TelegramUsers).values(
                tg_user_id = tg_user_id,
                tg_user_username = tg_user_username,
                tg_user_fullname = tg_user_fullname
            ).on_conflict_do_nothing(
                index_elements=["tg_user_id"]
            )

            await session.execute(stmt)
