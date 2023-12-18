from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text, Integer, BigInteger


class Base(DeclarativeBase):
    pass

class TelegramUsers(Base):
    __tablename__ = "telegram_users"
    tg_user_id:Mapped[int] = mapped_column(BigInteger, primary_key=True)
    tg_user_fullname: Mapped[str] = mapped_column(nullable=False)
    tg_user_username: Mapped[str] = mapped_column(nullable=True)

class TelegramChats(Base):
    __tablename__ = "telegram_chats"
    tg_chat_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, unique=True, primary_key=True
    )
    tg_chat_title: Mapped[str] = mapped_column(nullable=False)
    tg_chat_type: Mapped[str] = mapped_column(nullable=False)


class Participants(Base):
    __tablename__ = "participants"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    tg_user_firstname: Mapped[str] = mapped_column(nullable=False)

    tg_user_id: Mapped[int] = mapped_column(BigInteger,ForeignKey('telegram_users.tg_user_id'), nullable=False)
    tg_chat_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("telegram_chats.tg_chat_id"), nullable=False
    )

    def __str__(self):
        return f"Participant: {self.tg_user_firstname}"

    def __repr__(self):
        return f"Participant: {self.tg_user_firstname}"


class WishList(Base):
    __tablename__ = "wishlist"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_user_id: Mapped[int] = mapped_column(BigInteger,ForeignKey('telegram_users.tg_user_id'), nullable=False)
    
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    link: Mapped[str] = mapped_column(nullable=True)
    is_gift_received:Mapped[bool] = mapped_column(default=False,nullable=False)

    def __str__(self):
        return f"""
Название Подарка: {self.title}
Описание: {self.description}
"""


class Events(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    tg_receiver_id: Mapped[int] = mapped_column(BigInteger,ForeignKey('telegram_users.tg_user_id'), nullable=False)  # Кому дарит
    tg_santa_id: Mapped[int] = mapped_column(BigInteger,ForeignKey('telegram_users.tg_user_id'), nullable=False)  # Кто дарит
    tg_chat_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("telegram_chats.tg_chat_id"), nullable=False
    )
    is_gift_ready: Mapped[bool] = mapped_column(default=False,nullable=False)
