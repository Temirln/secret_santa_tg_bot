from sqlalchemy import delete, select, update

# from .db import session,get_async_session
from sqlalchemy.dialects.postgresql import insert

from ..models import Participants


async def delete_chat_participants(session, chat_id):
    async with session() as session:
        async with session.begin():
            stmt = delete(Participants).where(Participants.tg_chat_id == chat_id)
            await session.execute(stmt)


async def get_chat_participants(session, group_chat_id):
    async with session() as session:
        async with session.begin():
            stmt = select(Participants).where(Participants.tg_chat_id == group_chat_id)

            result = await session.execute(stmt)
            return result.scalars().fetchall()


async def add_participant(session, telegram_firstname, telegram_id, group_chat_id):
    async with session() as session:
        async with session.begin():
            new_participant = insert(Participants).values(
                tg_user_firstname=telegram_firstname,
                tg_user_id=telegram_id,
                tg_chat_id=group_chat_id,
            )
            await session.execute(new_participant)


async def get_participant(session, telegram_id, group_chat_id):
    async with session() as session:
        async with session.begin():
            stmt = select(Participants).where(
                Participants.tg_user_id == telegram_id,
                Participants.tg_chat_id == group_chat_id,
            )
            result = await session.execute(stmt)
            return result.scalars().one_or_none()


async def get_participant_groups(session, telegram_id):
    async with session() as session:
        async with session.begin():
            stmt = select(Participants).where(Participants.tg_user_id == telegram_id)
            result = await session.execute(stmt)

            return [
                participant.tg_chat_id for participant in result.scalars().fetchall()
            ]


async def delete_participant(session, telegram_id, group_chat_id):
    async with session() as session:
        async with session.begin():
            stmt = delete(Participants).where(
                Participants.tg_user_id == telegram_id,
                Participants.tg_chat_id == group_chat_id,
            )

            await session.execute(stmt)
