from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from config import DB_URI
from .models import Base

engine = create_async_engine(DB_URI, echo=True)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# async def get_async_session():
#     async with async_session_maker() as session:
#         yield session