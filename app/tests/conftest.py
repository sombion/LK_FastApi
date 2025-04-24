import asyncio
from datetime import datetime
import pytest
from sqlalchemy import insert
from app.config import settings
import json
from app.database import Base, async_session_maker, engine

from app.users.models import Users
from app.friends.models import Friends

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)
        
    users = open_mock_json("users")
    friends = open_mock_json("friends")
    
    async with async_session_maker() as session:
        add_users = insert(Users).values(users)
        add_friends = insert(Friends).values(friends)
        
        await session.execute(add_users)
        await session.execute(add_friends)
        
        await session.commit()
        
# Взято из документации к pytest-asyncio
# @pytest.fixture(scope="session")
# def event_loop(request):
#     """Create an instance of the default event loop for each test case."""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()