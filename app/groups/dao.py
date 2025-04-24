from sqlalchemy import delete, func, insert, select
from sqlalchemy.orm import aliased

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.groups.models import Groups, MembersGroup
from app.users.models import Users


class GroupDAO(BaseDAO):
    model = Groups
    
    @classmethod
    async def create(cls, title: str, description: str, id_created: int):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(
                title=title,
                description=description,
                id_created=id_created
            ).returning(cls.model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()
        
    @classmethod
    async def titles_with_members_count(cls):
        async with async_session_maker() as session:
            query = (
                select(
                    cls.model.id,
                    cls.model.title,
                    func.count(MembersGroup.id_user).label("members_count")
                )
                .outerjoin(MembersGroup, cls.model.id == MembersGroup.id_group)
                .group_by(cls.model.id, cls.model.title)
                .order_by(func.count(MembersGroup.id_user).desc())
                .limit(5)
            )
            result = await session.execute(query)
            return result.mappings().all()
    
class MemberGroupsDAO(BaseDAO):
    model = MembersGroup
    
    
    @classmethod
    async def find_group_in_user(cls, id_user):
        async with async_session_maker() as session:
            query = (
                select(cls.model.id_group, Groups.title)
                .join(Groups, cls.model.id_group == Groups.id)
                .where(cls.model.id_user == id_user)
            )
            result = await session.execute(query)
            return result.mappings().all()
    
    @classmethod
    async def create(cls, id_group: int, id_user: int):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(
               id_group=id_group,
               id_user=id_user
            ).returning(cls.model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()
       
    @classmethod
    async def delete_member(cls, id_group: int, id_user: int):
        async with async_session_maker() as session:
            stmt = delete(cls.model).where(
                cls.model.id_group==id_group,
                cls.model.id_user==id_user
            ).returning(cls.model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()
        
    @classmethod
    async def all_user_in_one_group(cls, id_group: int):
        async with async_session_maker() as session:
            query = (
                select(cls.model.__table__.columns, Users.login)
                .join(Users, cls.model.id_user == Users.id)
                .where(cls.model.id_group == id_group)
            )
            result = await session.execute(query)
            return result.mappings().all()
        
    @classmethod
    async def recommend_friends(cls, id_user: int):
        async with async_session_maker() as session:
            mg1 = aliased(cls.model)
            mg2 = aliased(cls.model)
            u = aliased(Users)

            query = (
                select(
                    u.id,
                    u.name,
                    u.login,
                    u.img,
                    func.count().label("common_groups")
                )
                .select_from(mg1)
                .join(mg2, mg1.id_group == mg2.id_group)
                .join(u, u.id == mg2.id_user)
                .where(
                    mg1.id_user == id_user,
                    mg2.id_user != id_user
                )
                .group_by(u.id)
                .order_by(func.count().desc())
                .limit(5)
            )

            result = await session.execute(query)
            return result.mappings().all()