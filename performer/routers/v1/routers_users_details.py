from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from performer.database import get_session
from performer.model.models import User_details
from performer.schemas.schemas_users_details import (
    DetailsList,
    UserDetailsFull,
)

Session_ = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix='/detail', tags=['Users', 'detail'])


@router.get('/', response_model=DetailsList, status_code=HTTPStatus.OK)
def get_info_user(session: Session_, skip: int = 0, limit: int = 100):
    db_details = session.scalars(
        select(User_details).offset(skip).limit(limit)
    ).all()

    return {'details': db_details}


@router.get(
    '/{user_id}', response_model=UserDetailsFull, status_code=HTTPStatus.OK
)
def get_info_user_by_id(user_id: int, session: Session_):
    db_details = session.scalar(
        select(User_details).where(User_details.user_id == user_id)
    )
    if not db_details:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Informações não encontrado',
        )
    return db_details


@router.put('/')
def add_info_user(session: Session_):
    return True
