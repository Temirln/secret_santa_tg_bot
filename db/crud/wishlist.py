from ..models import WishList

# from .db import session,get_async_session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, delete, update



async def delete_user_wish(session, wish_id):
    async with session() as session:
        async with session.begin():
            stmt = delete(WishList).where(
                WishList.id == wish_id
            )

            await session.execute(stmt)

async def get_user_wishes(session, user_tg_id):
    async with session() as session:
        async with session.begin():
            stmt = select(WishList).where(
                WishList.tg_user_id == user_tg_id
            )
            result = await session.execute(stmt)
            return result.scalars().fetchall()


async def add_user_wish(session, user_tg_id, wish_data):
    async with session() as session:
        async with session.begin():
            stmt = insert(WishList).values(
                tg_user_id=user_tg_id,
                title=wish_data["title"],
                link=wish_data["link"],
                description=wish_data["desc"],
            )

            await session.execute(stmt)

async def update_user_wish(session,user_tg_id, wish_id):
    async with session() as session:
        async with session.begin():
            stmt = update(WishList).where(
                WishList.tg_user_id == user_tg_id,
                WishList.id == wish_id
            ).values(
                is_gift_received = True
            )

            await session.execute(stmt)
