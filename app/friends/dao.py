from sqlalchemy import and_, delete, insert, or_, select, union, update
from sqlalchemy.orm import aliased

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.friends.models import Friends
from app.users.models import Users


class FriendsDAO(BaseDAO):
    model = Friends


    @classmethod
    async def detail_friends(cls, id_user: int, id_friends: int):
        async with async_session_maker() as session:
            u1 = aliased(Users)
            u2 = aliased(Users)
            query = (
                select(cls.model.__table__.columns, u1.id, u1.login, u1.img, u2.id, u2.login, u2.img)
                .join(u1, u1.id==cls.model.id_user)
                .join(u2, u2.id==cls.model.id_friends)
                .where(
                    or_(
                        and_(cls.model.id_user==id_user, cls.model.id_friends==id_friends),
                        and_(cls.model.id_user==id_friends, cls.model.id_friends==id_user)
                    ),
                    cls.model.status_user==True,
                    cls.model.status_friends==True
                )
            )
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def my_friends(cls, id_user: int):
        async with async_session_maker() as session:
            f1 = aliased(Friends)
            f2 = aliased(Friends)

            subquery_friends = (
                union(
                    select(f1.id_friends).where(f1.id_user == id_user, f1.status_friends == True),
                    select(f2.id_user).where(f2.id_friends == id_user, f2.status_friends == True),
                ).subquery()
            )

            query = (
                select(Users.id, Users.name, Users.login)
                .where(
                    Users.id.in_(select(subquery_friends.c.id_friends)),
                    Users.id != id_user
                )
            )
            result = await session.execute(query)
            return result.mappings().all()
        
    @classmethod
    async def invite_friends(cls, id_user: int, id_friends: int):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(
                id_user = id_user,
                id_friends = id_friends
            ).returning(cls.model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()
            
    @classmethod
    async def check_invite_list_friends(cls, id_user: int, id_friends: int) -> Friends:
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .join(Users, Users.id==cls.model.id_user)
                .where(
                    cls.model.id_user==id_friends,
                    cls.model.id_friends==id_user,
                    cls.model.status_user==True,
                    cls.model.status_friends==False,
                )
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def invite_list_friends(cls, id_user: int):
        async with async_session_maker() as session:
            query = (
                select(cls.model.__table__.columns, Users.login, Users.name)
                .join(Users, Users.id==cls.model.id_user)
                .where(
                    cls.model.id_friends==id_user,
                    cls.model.status_user==True,
                    cls.model.status_friends==False,
                )
            )
            result = await session.execute(query)
            return result.mappings().all()
        
    @classmethod
    async def accept_friends(cls, id_user: int, id_friends: int):
        async with async_session_maker() as session:
            stmt = (
                update(cls.model)
                .where(
                    or_(
                        and_(cls.model.id_user==id_user, cls.model.id_friends==id_friends),
                        and_(cls.model.id_user==id_friends, cls.model.id_friends==id_user)
                    )
                )
                .values(status_friends=True)
                .returning(cls.model))
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()
        
    @classmethod
    async def delete_friends(cls, id_user: int, id_friends: int):
        async with async_session_maker() as session:
            stmt = delete(cls.model).where(
                or_(
                    and_(
                        cls.model.id_user == id_user,
                        cls.model.id_friends == id_friends
                    ),
                    and_(
                        cls.model.id_user == id_friends,
                        cls.model.id_friends == id_user 
                    )
                ),
                cls.model.status_user == True,
                cls.model.status_friends == True
            ).returning(cls.model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()
            
    @classmethod
    async def reject_friends(cls, id_user: int, id_friends: int):
        async with async_session_maker() as session:
            stmt = delete(cls.model).where(
                and_(
                    cls.model.id_user == id_friends,
                    cls.model.id_friends == id_user,
                    cls.model.status_user == True,
                    cls.model.status_friends == False
                )
            ).returning(cls.model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()
        
    @classmethod
    async def list_possible_friends(cls, id_user: int):
        async with async_session_maker() as session:
            f1 = aliased(Friends)
            f2 = aliased(Friends)

            subquery_friends = (
                union(
                    select(f1.id_friends).where(f1.id_user == id_user),
                    select(f2.id_user).where(f2.id_friends == id_user),
                ).subquery()
            )

            query = (
                select(Users.id, Users.name, Users.login)
                .where(
                    ~Users.id.in_(select(subquery_friends.c.id_friends)),
                    Users.id != id_user
                )
            )
            
            result = await session.execute(query)
            return result.mappings().all()
        
    @classmethod
    async def check_friends_or_invite(cls, id_user: int, id_friends: int):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .where(
                    or_(
                        and_(cls.model.id_user == id_user, cls.model.id_friends == id_friends),
                        and_(cls.model.id_user == id_friends, cls.model.id_friends == id_user 
                        )
                    )
                )
            )
            result = await session.execute(query)
            return result.mappings().all()
        
    @classmethod
    async def check_friends(cls, id_user: int, id_friends: int):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .where(
                    or_(
                        and_(cls.model.id_user == id_user, cls.model.id_friends == id_friends),
                        and_(cls.model.id_user == id_friends, cls.model.id_friends == id_user 
                        )
                    ),
                    cls.model.status_user==True,
                    cls.model.status_friends==True
                )
            )
            result = await session.execute(query)
            return result.mappings().all()