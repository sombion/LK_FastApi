from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    name: Mapped[str]
    login: Mapped[str]
    hash_password: Mapped[str]
    img: Mapped[str]
    email: Mapped[str] = mapped_column(nullable=True)

    count_login: Mapped[int] = mapped_column(default=0, nullable=False, server_default="0")

    user: Mapped[bool] = mapped_column(default=True)
    admin: Mapped[bool] = mapped_column(default=False)