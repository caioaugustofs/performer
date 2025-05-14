from http import HTTPStatus
from typing import Annotated

import toml
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from performer.database import get_session
from performer.model.models import Workouts
from performer.schemas.workout.schemas_workout import (
    WorkoutCreate,
    WorkoutFull,
    WorkoutPublic,
    WorkoutPublicList,
    WorkoutUpdate,
)
from performer.tools.tool_logs import logger

router = APIRouter(prefix='/workouts', tags=['Workouts'])

Session = Annotated[AsyncSession, Depends(get_session)]
config = toml.load(r'performer/docs/workout/routers_workout.toml')


# ------------------------- GET -------------------------#


@router.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=WorkoutPublicList,
    summary=config['get_workouts']['summary'],
    description=config['get_workouts']['description'],
    response_description=config['get_workouts']['resp_description'],
)
async def get_workouts(session: Session, skip: int = 0, limit: int = 100):
    workouts = await session.scalars(
        select(Workouts).offset(skip).limit(limit)
    )
    logger.info('rota utilizada get_workouts')
    return {'workouts': workouts.all()}


@router.get(
    '/{workout_id}',
    status_code=HTTPStatus.OK,
    response_model=WorkoutFull,
    summary=config['get_workout_by_id']['summary'],
    description=config['get_workout_by_id']['description'],
    response_description=config['get_workout_by_id']['resp_description'],
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
    summary=config['get_public_status']['summary'],
    description=config['get_public_status']['description'],
    response_description=config['get_public_status']['resp_description'],
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
    summary=config['get_by_Workouts']['summary'],
    description=config['get_by_Workouts']['description'],
    response_description=config['get_by_Workouts']['resp_description'],
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
    summary=config['get_workouts_by_user_and_public_status']['summary'],
    description=config['get_workouts_by_user_and_public_status'][
        'description'
    ],
    response_description=config['get_workouts_by_user_and_public_status'][
        'resp_description'
    ],
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


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=WorkoutPublic,
    summary=config['create_workout']['summary'],
    description=config['create_workout']['description'],
    response_description=config['create_workout']['resp_description'],
)
async def create_workout(workout: WorkoutCreate, session: Session):
    db_workout = Workouts(
        name=workout.name,
        duration_min=workout.duration_min,
        is_public=workout.is_public,
        difficulty=workout.difficulty,
        type=workout.type,
        rest_between_exercises_seconds=workout.rest_between_exercises_seconds,
        created_by=1,
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
    summary=config['update_workout']['summary'],
    description=config['update_workout']['description'],
    response_description=config['update_workout']['resp_description'],
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
@router.delete(
    '/{user_id}/{workout_id}',
    status_code=HTTPStatus.NO_CONTENT,
    summary=config['delete_workout']['summary'],
    description=config['delete_workout']['description'],
    response_description=config['delete_workout']['resp_description'],
)
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
