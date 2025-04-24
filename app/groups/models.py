from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Groups(Base):
    __tablename__ = "groups"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    id_created: Mapped[int] = mapped_column(ForeignKey("users.id"))
    

class MembersGroup(Base):
    __tablename__ = "members_group"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    id_group: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))