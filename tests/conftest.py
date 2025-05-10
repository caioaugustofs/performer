import random
from contextlib import contextmanager
from datetime import datetime

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from performer.app import app
from performer.database import get_session
from performer.model.models import User, User_details, table_registry


@pytest_asyncio.fixture
def client(session):
    async def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest_asyncio.fixture
async def user(session):
    user = User(username='Teste', email='teste@test.com', password='testtest')
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@pytest_asyncio.fixture
async def user_details(session, user):
    details = User_details(user_id=user.id, data_de_nascimento='01/01/2000')

    session.add(details)
    await session.commit()
    await session.refresh(details)
    return details


@pytest.fixture
def user_factory(session):
    class UserFactory:
        @staticmethod
        def create_batch(count, **kwargs):
            users = []
            for _ in range(count):
                user = User(
                    username=f'user{random.randint(1, 10000)}',
                    email=f'user{random.randint(1, 10000)}@test.com',
                    password='password',
                    email_verified=kwargs.get('email_verified', False),
                )
                session.add(user)
                users.append(user)
            session.commit()
            return users

    return UserFactory()
