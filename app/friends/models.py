from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.database import Base

class Friends(Base):
    __tablename__ = "friends"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    id_friends: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status_user: Mapped[bool] = mapped_column(default=True)
    status_friends: Mapped[bool] = mapped_column(default=False)