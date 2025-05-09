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


@pytest.mark.asyncio
async def test_update_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        # Criação de um novo usuário
        new_user = User(
            username='bob',
            password='password123',
            email='bob@test.com',
            last_login=time,
        )
        session.add(new_user)
        await session.commit()

    # Atualização do usuário
    user = await session.scalar(select(User).where(User.username == 'bob'))
    user.email = 'bob_updated@test.com'
    await session.commit()

    # Verificação da atualização
    updated_user = await session.scalar(
        select(User).where(User.username == 'bob')
    )
    assert updated_user.email == 'bob_updated@test.com'


@pytest.mark.asyncio
async def test_delete_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        # Criação de um novo usuário
        new_user = User(
            username='charlie',
            password='delete_me',
            email='charlie@test.com',
            last_login=time,
        )
        session.add(new_user)
        await session.commit()

    # Exclusão do usuário
    user = await session.scalar(select(
        User).where(User.username == 'charlie'))
    await session.delete(user)
    await session.commit()

    # Verificação da exclusão
    deleted_user = await session.scalar(
        select(User).where(User.username == 'charlie'))
    assert deleted_user is None
