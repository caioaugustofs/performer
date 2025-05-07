from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from performer.database import get_session
from performer.models import User
from performer.schemas.schemas_users import (
    UserCreateSchema,
    UserList,
    UserPasswordUpdate,
    UserPublicSchema,
    UserUsernameUpdate,
)

router = APIRouter(prefix='/users', tags=['Users'])

Session_ = Annotated[Session, Depends(get_session)]


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=UserPublicSchema
)
def create_user(user: UserCreateSchema, session: Session_):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )

    db_user = User(**user.dict())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def get_users(session: Session_, skip: int = 0, limit: int = 100):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@router.get(
    '/{user_id}', response_model=UserPublicSchema, status_code=HTTPStatus.OK
)
def get_user_by_id(user_id: int, session: Session_):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    return db_user


@router.patch(
    '/password/{user_id}',
    response_model=UserPublicSchema,
    status_code=HTTPStatus.OK,
)
def update_password(user_id: int, user: UserPasswordUpdate, session: Session_):
    db_user = session.scalar(
        select(User).where(or_(User.id == user_id, User.email == user.email))
    )

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    if db_user.password == user.password:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Vocẽ já possui essa senha',
        )

    db_user.password = user.new_password
    session.commit()
    session.refresh(db_user)
    return db_user


@router.patch(
    '/username/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublicSchema,
)
def update_username(user_id: int, user: UserUsernameUpdate, session: Session_):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    if db_user.username == user.new_username:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Vocẽ já possui esse username',
        )

    db_user.username = user.new_username
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete('/{user_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int, session: Session_):
    db_user = session.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    session.delete(db_user)
    session.commit()
