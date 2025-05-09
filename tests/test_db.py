import pytest
from sqlalchemy import select

from performer.model.models import User


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='alice',
            password='secret',
            email='teste@test',
            last_login=time,
        )
        session.add(new_user)
        await session.commit()

    user = await session.scalar(select(User).where(User.username == 'alice'))

    assert {
        'id': user.id,
        'username': user.username,
        'password': user.password,
        'email': user.email,
        'created_at': user.created_at,
    } == {
        'id': 1,
        'username': 'alice',
        'password': 'secret',
        'email': 'teste@test',
        'created_at': time,
    }
