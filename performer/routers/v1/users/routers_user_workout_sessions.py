from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from performer.database import get_session
from performer.model.models import User_Workout_Sessions

router = APIRouter(prefix='/Workout_Sessions', tags=['Workout Sessions'])

Session = Annotated[AsyncSession, Depends(get_session)]


@router.get('/', status_code=HTTPStatus.OK)
async def get_user_workout_sessions(session: Session):
    workout_sessions = await session.scalars(select(User_Workout_Sessions))
    return workout_sessions


@router.get('/{user_id}', status_code=HTTPStatus.OK)
async def get_user_workout_sessions_by_id(user_id: int, session: Session):
    workout_sessions = await session.scalars(
        select(User_Workout_Sessions).where(
            User_Workout_Sessions.user_id == user_id
        )
    )

    return workout_sessions
