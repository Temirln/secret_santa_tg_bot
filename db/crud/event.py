from ..models import Events

# from .db import session,get_async_session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, delete, update


async def delete_group_events(session, chat_id):
    async with session() as session:
        async with session.begin():
            stmt = delete(Events).where(
                Events.tg_chat_id == chat_id
            )
            await session.execute(stmt)

async def update_event_receiveer_giver(session, receiver_id, giver_id, chat_id):
    async with session() as session:
        async with session.begin():
            stmt = (
                update(Events)
                .where(
                    Events.tg_receiver_id == receiver_id,
                    Events.tg_chat_id == chat_id,
                    Events.tg_santa_id == giver_id,
                )
                .values(is_gift_ready=True)
            )
            await session.execute(stmt)


async def get_santa_chat_event(session, santa_id, chat_id):
    async with session() as session:
        async with session.begin():
            stmt = select(Events).where(
                Events.tg_santa_id == santa_id, Events.tg_chat_id == chat_id
            )

            result = await session.execute(stmt)
            return result.scalars().one_or_none()


async def get_receiver_chat_event(session, receiver_id, chat_id):
    async with session() as session:
        async with session.begin():
            stmt = select(Events).where(
                Events.tg_receiver_id == receiver_id, Events.tg_chat_id == chat_id
            )

            result = await session.execute(stmt)
            return result.scalars().one_or_none()

async def get_santa_event(session, giver_id):
    async with session() as session:
        async with session.begin():
            stmt = select(Events).where(
                Events.tg_santa_id == giver_id,
            )
            result = await session.execute(stmt)
            return result.scalars().fetchall()

            
async def get_receiver_event(session, receiver_id):
    async with session() as session:
        async with session.begin():
            stmt = select(Events).where(
                Events.tg_receiver_id == receiver_id
            )

            result = await session.execute(stmt)
            return result.scalars().fetchall()
        
    
async def get_chat_event(session, chat_id):
    async with session() as session:
        async with session.begin():
            stmt = select(Events).where(
                Events.tg_chat_id == chat_id
            )
            result = await session.execute(stmt)
            return result.scalars().fetchall()
        

async def arrange_all_giver_receiver(session, giver_id, receiver_id, chat_id):
    async with session() as session:
        async with session.begin():
            stmt = insert(Events).values(
                tg_chat_id=chat_id, tg_receiver_id=receiver_id, tg_santa_id=giver_id
            )
            await session.execute(stmt)