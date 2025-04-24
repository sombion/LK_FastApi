from sqlalchemy import insert, update

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.users.models import Users


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def create_user(
            cls,
            name: str,
            login: str,
            hash_password: str,
            email: str
        ):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(
                name = name,
                login = login,
                hash_password = hash_password,
                img = "app/static/img/default.png",
                email = email
            ).returning(cls.model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()

    @classmethod
    async def edit_password(cls, id: int, new_password: str):
        async with async_session_maker() as session:
            stmt = (
                update(cls.model)
                .where(cls.model.id==id)
                .values(hash_password=new_password)
                .returning(cls.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()


    @classmethod
    async def upgrade_visit_count(cls, id):
        async with async_session_maker() as session:
            stmt = (
                update(cls.model)
                .where(cls.model.id==id)
                .values(count_login = cls.model.count_login + 1)
                .returning(cls.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()

    @classmethod
    async def upgrade_img(cls, id: int, url: str):
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id==id).values(img=url).returning(cls.model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()