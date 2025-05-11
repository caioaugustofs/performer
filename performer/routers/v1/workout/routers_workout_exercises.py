from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from performer.database import get_session
from performer.model.models import Workout_Exercises
from performer.tools.tool_logs import logger

router = APIRouter(
    prefix='/workouts/workout-exercises',
    tags=['Workout Exercises'],
)

Session = Annotated[AsyncSession, Depends(get_session)]


# ------------------------- GET -------------------------#
@router.get('/')
async def get_workout_exercises(session: Session):
    workout_exercises = await session.scalars(select(Workout_Exercises))

    if not workout_exercises:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Workout Exercises não encontrado',
        )
    logger.info('rota utilizada get_workout_exercises')
    return workout_exercises.all()


# ------------------------- POST -------------------------#
# ------------------------- PATCH -------------------------#
# ------------------------- DELETE -------------------------#
