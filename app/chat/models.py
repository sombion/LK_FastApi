from datetime import datetime

from sqlalchemy import Date, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Chats(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    id_friends: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    id_group: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=True)


class Messages(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    text_message: Mapped[str]
    date_send: Mapped[datetime] = mapped_column(Date, nullable=True, default=func.now())
    id_chat: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    id_send_user: Mapped[int] = mapped_column(ForeignKey("users.id"))