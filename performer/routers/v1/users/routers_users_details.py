from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from performer.database import get_session
from performer.model.models import User_details
from performer.schemas.users.schemas_users_details import (
    DetailsList,
    UseDetailsPicture,
    UseDetailsPictureResponse,
    UserDetailsFull,
    UserDetailsPublic,
    UserDetailsUpdate,
)

Session = Annotated[AsyncSession, Depends(get_session)]


router = APIRouter(prefix='/detail', tags=['Detail'])

# ------------------------- GET -------------------------#


@router.get('/', response_model=DetailsList, status_code=HTTPStatus.OK)
async def get_info_user(session: Session, skip: int = 0, limit: int = 100):
    db_details = await session.scalars(
        select(User_details).offset(skip).limit(limit)
    )
    if not db_details:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Informações não encontrado',
        )

    return {'details': db_details}


@router.get(
    '/{user_id}', response_model=UserDetailsFull, status_code=HTTPStatus.OK
)
async def get_info_user_by_id(user_id: int, session: Session):
    db_details = await session.scalar(
        select(User_details).where(User_details.user_id == user_id)
    )
    if not db_details:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Informações não encontrado',
        )
    return db_details


# ------------------------- PATCH -------------------------#


@router.patch('/', response_model=UserDetailsPublic, status_code=HTTPStatus.OK)
async def update_info_user(user_info: UserDetailsUpdate, session: Session):
    db_details = await session.scalar(
        select(User_details).where(User_details.user_id == user_info.user_id)
    )

    if not db_details:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Informações não encontrado',
        )

    for key, value in user_info.dict().items():
        setattr(db_details, key, value)

    session.commit()
    await session.refresh(db_details)
    return db_details


@router.patch(
    '/picture',
    response_model=UseDetailsPictureResponse,
    status_code=HTTPStatus.OK,
)
async def update_info_user_picture(
    user_info: UseDetailsPicture, session: Session
):
    db_details = await session.scalar(
        select(User_details).where(User_details.user_id == user_info.user_id)
    )

    if not db_details:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Informações não encontrado',
        )

    db_details.profile_picture_url = user_info.profile_picture_url

    await session.commit()
    await session.refresh(db_details)
    return db_details
