from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from performer.database import get_session
from performer.model.models import Workouts
from performer.schemas.workout.schemas_workout import (
    WorkoutFull,
    WorkoutPublic,
    WorkoutPublicList,
    WorkoutUpdate,
)
from performer.tools.tool_logs import logger

router = APIRouter(prefix='/workouts', tags=['Workouts'])

Session = Annotated[AsyncSession, Depends(get_session)]


# ------------------------- GET -------------------------#


@router.get('/', status_code=HTTPStatus.OK, response_model=WorkoutPublicList)
async def get_workouts(session: Session, skip: int = 0, limit: int = 100):
    workouts = await session.scalars(
        select(Workouts).offset(skip).limit(limit)
    )
    logger.info('rota utilizada get_workouts')
    return {'workouts': workouts.all()}


@router.get(
    '/{workout_id}', status_code=HTTPStatus.OK, response_model=WorkoutFull
)
async def get_workout_by_id(workout_id: int, session: Session):
    db_workout = await session.scalar(
        select(Workouts).where(Workouts.id == workout_id)
    )

    if not db_workout:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Workout não encontrado'
        )
    logger.info('rota utilizada get_workout_by_id')
    return db_workout


@router.get(
    '/public/{public_status}',
    status_code=HTTPStatus.OK,
    response_model=WorkoutPublicList,
)
async def get_public_status(public_status: bool, session: Session):
    workouts = await session.scalars(
        select(Workouts).where(Workouts.is_public == public_status)
    )

    workouts_list = workouts.all()

    if not workouts_list:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Não foi encontrado nenhuma \
workout com public={public_status}',
        )
    logger.info('rota utilizada get_public_status')
    return {'workouts': workouts_list}


@router.get(
    '/created_by/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=WorkoutPublicList,
)
async def get_by_Workouts(user_id: int, session: Session):
    workouts = await session.scalars(
        select(Workouts).where(Workouts.created_by == user_id)
    )

    workouts_list = workouts.all()

    if not workouts_list:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Nada encontrado',
        )
    logger.info('rota utilizada get_by_Workouts')
    return {'workouts': workouts_list}


@router.get(
    '/created_by/{user_id}/public/{public_status}',
    status_code=HTTPStatus.OK,
    response_model=WorkoutPublicList,
)
async def get_workouts_by_user_and_public_status(
    user_id: int, public_status: bool, session: Session
):
    workouts = await session.scalars(
        select(Workouts).where(
            and_(
                Workouts.created_by == user_id,
                Workouts.is_public == public_status,
            )
        )
    )

    workouts_list = workouts.all()

    if not workouts_list:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'No workouts found with public_status={public_status}\
 for user_id={user_id}',
        )
    logger.info('rota utilizada get_workouts_by_user_and_public_status')

    return {'workouts': workouts_list}


# ------------------------- POST -------------------------#


@router.post('/', status_code=HTTPStatus.CREATED, response_model=WorkoutPublic)
async def create_workout(workout: WorkoutFull, session: Session):
    db_workout = Workouts(
        name=workout.name,
        duration_min=workout.duration_min,
        is_public=workout.is_public,
        difficulty=workout.difficulty,
        type=workout.type,
        rest_between_exercises_seconds=workout.rest_between_exercises_seconds,
        created_by=workout.created_by,
    )

    session.add(db_workout)
    await session.commit()
    await session.refresh(db_workout)

    logger.info('rota utilizada create_workout')
    return db_workout


# ------------------------- PATCH -------------------------#


@router.patch(
    '/{user_id}/{workout_id}',
    status_code=HTTPStatus.OK,
    response_model=WorkoutPublic,
)
async def update_workout(
    workout_id: int, user_id: int, workout: WorkoutUpdate, session: Session
):
    db_workout = await session.scalar(
        select(Workouts).where(
            Workouts.id == workout_id, Workouts.created_by == user_id
        )
    )

    if not db_workout:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Workout não encontrado'
        )

    for key, value in workout.dict().items():
        setattr(db_workout, key, value)

    await session.commit()
    await session.refresh(db_workout)
    logger.info('rota utilizada update_workout')

    return db_workout


# ------------------------- DELETE -------------------------#
@router.delete('/{user_id}/{workout_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_workout(workout_id: int, user_id: int, session: Session):
    db_workout = await session.scalar(
        select(Workouts).where(
            Workouts.id == workout_id, Workouts.created_by == user_id
        )
    )

    if not db_workout:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Workout não encontrado'
        )

    await session.delete(db_workout)
    await session.commit()
