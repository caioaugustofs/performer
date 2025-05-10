from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from performer.database import get_session
from performer.model.models import User
from performer.schemas.users.schemas_users import (
    ResponseRole,
    ResponseSubscriptionStatus,
    UserCreateSchema,
    UserList,
    UserPasswordUpdate,
    UserPublicSchema,
    UserUsernameUpdate,
    returnSubscriptionList,
)
from performer.tools.tool_logs import logger

router = APIRouter(prefix='/users', tags=['Users'])

Session = Annotated[AsyncSession, Depends(get_session)]

# ------------------------- POST -------------------------#


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=UserPublicSchema
)
async def create_user(user: UserCreateSchema, session: Session):
    db_user = await session.scalar(
        select(User).where(
            or_(User.username == user.username, User.email == user.email)
        )
    )

    if db_user:
        logger.warning('Usuário já existe')
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )

    db_user = User(**user.dict())
    session.add(db_user)

    await session.commit()
    await session.refresh(db_user)
    logger.info('rota utilizada create_user POST')
    return db_user


# ------------------------- GET -------------------------#


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
async def get_users(session: Session, skip: int = 0, limit: int = 100):
    users = await session.scalars(select(User).offset(skip).limit(limit))
    logger.info('rota utilizada get_users')
    return {'users': users.all()}


@router.get(
    '/{user_id}',
    response_model=UserPublicSchema,
    status_code=HTTPStatus.OK,
)
async def get_user_by_id(user_id: int, session: Session):
    db_user = await session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )
    logger.info('rota utilizada get_user_by_id')
    return db_user


# se o email é verificado ou nao
@router.get(
    '/email_verified/{verified}',
    response_model=UserList,
    status_code=HTTPStatus.OK,
)
async def get_user_by_email_verified(
    session: Session,
    email_verified: bool = False,
    skip: int = 0,
    limit: int = 100,
):
    users = await session.scalars(
        select(User)
        .where(User.email_verified == email_verified)
        .offset(skip)
        .limit(limit)
    )

    if not users:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )
    logger.info('rota utilizada get_user_by_email_verified')

    return {'users': users.all()}


@router.get(
    '/subscription_status/{status}',
    status_code=HTTPStatus.OK,
    response_model=returnSubscriptionList,
)
async def get_user_by_status(
    status: str, session: Session, skip: int = 0, limit: int = 100
):
    users = await session.scalars(
        select(User)
        .where(User.subscription_status == status)
        .offset(skip)
        .limit(limit)
    )

    if not users:
        logger.warning(f'Usuários com status={status} não encontrados')
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuários não encontrados'
        )

    numero_user = len(users.all())
    logger.info('rota utilizada get_user_by_status')
    return {'total': numero_user, 'subscription_status': users.all()}


# ------------------------- PATCH -------------------------#


@router.patch(
    '/password/{user_id}',
    response_model=UserPublicSchema,
    status_code=HTTPStatus.OK,
)
async def update_password(
    user_id: int, user: UserPasswordUpdate, session: Session
):
    db_user = await session.scalar(
        select(User).where(or_(User.id == user_id, User.email == user.email))
    )

    if not db_user:
        logger.warning('Usuário não encontrado')
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
              detail='Usuário não encontrado'
        )

    if db_user.password == user.new_password:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Vocẽ já possui essa senha',
        )

    db_user.password = user.new_password
    await session.commit()
    await session.refresh(db_user)
    logger.info('rota utilizada update_password')
    return db_user


@router.patch(
    '/username/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublicSchema,
)
async def update_username(
    user_id: int, user: UserUsernameUpdate, session: Session
):
    db_user = await session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        logger.warning('Usuário não encontrado')
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    if db_user.username == user.new_username:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Vocẽ já possui esse username',
        )

    db_user.username = user.new_username
    await session.commit()
    await session.refresh(db_user)
    logger.info('rota utilizada update_username')
    return db_user


@router.patch(
    '/role/{user_id}/{role}',
    response_model=ResponseRole,
    status_code=HTTPStatus.OK,
)
async def user_update_role(user_id: int, role: str, session: Session):
    db_user = await session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        logger.warning('Usuário não encontrado')
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    if db_user.role == role:
        logger.warning('Usuário já possui esse papel')
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Vocẽ já possui esse papel',
        )

    db_user.role = role
    await session.commit()
    await session.refresh(db_user)
    logger.info('rota utilizada update_role')
    return db_user


@router.patch(
    '/subscription_status/{user_id}',
    response_model=ResponseSubscriptionStatus,
    status_code=HTTPStatus.OK,
)
async def user_update_Subscription_Status(
    user_id: int, user_info: ResponseSubscriptionStatus, session: Session
):
    db_user = await session.scalar(
        select(User).where(
            or_(User.id == user_id, User.email == user_info.email)
        )
    )

    if not db_user:
        logger.warning('Usuário não encontrado')
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    if db_user.subscription_status == user_info.subscription_status:
        logger.warning('Usuário já possui esse status')
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Vocẽ já possui esse status',
        )

    db_user.subscription_status = user_info.subscription_status
    await session.commit()
    await session.refresh(db_user)
    logger.info('rota utilizada update_Subscription_Status')
    return db_user


# ------------------------- DELETE -------------------------#


@router.delete('/delete/{user_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_user(user_id: int, session: Session):
    db_user = await session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    await session.delete(db_user)
    await session.commit()
    logger.info(f'rota utilizada delete_user DELETE user_id:{user_id}')
