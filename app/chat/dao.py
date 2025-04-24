from sqlalchemy import and_, case, delete, insert, or_, select
from sqlalchemy.orm import aliased

from app.chat.models import Chats, Messages
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.groups.models import Groups, MembersGroup
from app.users.models import Users


class ChatDAO(BaseDAO):
    model = Chats
    
    @classmethod
    async def detail_info_chat_friends(cls, id_chat):
        async with async_session_maker() as session:
            u1 = aliased(Users)
            u2 = aliased(Users)
            query = (
                select(cls.model.__table__.columns, u1.id, u1.login, u1.img, u2.id, u2.login, u2.img)
                .join(u1, cls.model.id_user==u1.id)
                .join(u2, cls.model.id_friends==u2.id)
                .where(cls.model.id==id_chat)
            )
            result = await session.execute(query)
            return result.mappings().all()
        
    @classmethod
    async def my_chats(cls, id_user: int):
        async with async_session_maker() as session:
            interlocutor_id = case(
                (cls.model.id_user == id_user, cls.model.id_friends),
                else_=cls.model.id_user
            ).label("interlocutor_id")

            query = (
                select(cls.model.__table__.columns, interlocutor_id, Users.__table__.columns)
                .join(Users, interlocutor_id==Users.id)
                .where(
                    or_(
                        cls.model.id_user == id_user,
                        cls.model.id_friends == id_user
                    )
                )
            )
            result = await session.execute(query)
            return result.mappings().all()
    
    @classmethod
    async def my_group_chats(cls, user_id):
        async with async_session_maker() as session:
            group_ids_subq = (
                select(Groups.id, Groups.title)
                .join(MembersGroup, Groups.id == MembersGroup.id_group, isouter=True)
                .where(
                    or_(
                        Groups.id_created == user_id,
                        MembersGroup.id_user == user_id
                    )
                )
                .distinct()
                .subquery()
            )

            group_chats = (
                select(cls.model.__table__.columns, group_ids_subq.c.title)
                .where(cls.model.id_group.in_(select(group_ids_subq.c.id)))
            )
            result = await session.execute(group_chats)
            return result.mappings().all()
    
    @classmethod
    async def search_chat_two_user(cls, id_user: int, id_friends: int):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .where(
                    or_(
                        and_(cls.model.id_user==id_user, cls.model.id_friends==id_friends),
                        and_(cls.model.id_user==id_friends, cls.model.id_friends==id_user)
                    )
                )
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()
    
    @classmethod
    async def create(cls, id_user: int | None, id_friends: int | None, id_group: int | None):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(
                id_user=id_user,
                id_friends=id_friends,
                id_group=id_group
            ).returning(cls.model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()
    
    @classmethod
    async def delete(cls, id_chat: int):
        async with async_session_maker() as session:
            stmt = (
                delete(cls.model)
                .where(cls.model.id==id_chat)
                .returning(cls.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()
    
    @classmethod
    async def detail_info_chat_group(cls, id_chat: int):
        async with async_session_maker() as session:
            stmt = (
                select(
                    Groups.id.label("group_id"),
                    Groups.title.label("group_title"),
                    Groups.description.label("group_description"),
                    Users.id.label("owner_id"),
                    Users.name.label("owner_name")
                )
                .join(Chats, Chats.id_group == Groups.id)
                .join(Users, Groups.id_created == Users.id)
                .where(Chats.id == id_chat)
                .limit(1)
            )
            result = await session.execute(stmt)
            return result.mappings().all()
    
class MessagesDAO(BaseDAO):
    model = Messages
    
    @classmethod
    async def detail(cls, id_chat: int):
        async with async_session_maker() as session:
            query = (
                select(cls.model.__table__.columns, Users.login)
                .join(Users, cls.model.id_send_user==Users.id)
                .where(cls.model.id_chat==id_chat)
                .order_by(cls.model.id)
            )
            result = await session.execute(query)
            return result.mappings().all()
    
    @classmethod
    async def create(cls, text_message: str, id_chat: int, id_send_user: int):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(
                text_message=text_message,
                id_chat=id_chat,
                id_send_user=id_send_user
            ).returning(cls.model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()
    
    @classmethod
    async def delete(cls, id_chat: int):
        async with async_session_maker() as session:
            stmt = delete(cls.model).where(cls.model.id==id_chat).returning()
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()