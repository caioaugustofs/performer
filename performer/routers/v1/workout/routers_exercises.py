from http import HTTPStatus
from typing import Annotated, List

import toml
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from performer.database import get_session
from performer.model.models import Exercises
from performer.schemas.workout.schemas_exercises import (
    ExerciseCreate,
    ExercisePublic,
    ExercisePublicList,
    ExerciseUpdate,
    ExerciseUpdateMidia,
)
from performer.tools.tool_logs import logger

config = toml.load(r'performer/docs/workout/routers_exercises.toml')

router = APIRouter(prefix='/exercises', tags=['Exercises'])

Session = Annotated[AsyncSession, Depends(get_session)]


# ------------------------- GET -------------------------#
@router.get(
    '/',
    response_model=ExercisePublicList,
    status_code=HTTPStatus.OK,
    summary=config['get_exercises']['summary'],
    description=config['get_exercises']['description'],
    response_description=config['get_exercises']['resp_description'],
)
async def get_exercises(
    session: Session,
):
    result = await session.execute(select(Exercises))
    exercises = result.scalars().all()
    return {'exercises': exercises}


@router.get(
    '/{difficulty}',
    response_model=ExercisePublicList,
    status_code=HTTPStatus.OK,
    summary=config['get_exercises_difficulty']['summary'],
    description=config['get_exercises_difficulty']['description'],
    response_description=config['get_exercises_difficulty'][
        'resp_description'
    ],
)
async def get_exercises_difficulty(difficulty: int, session: Session):
    result = await session.execute(
        select(Exercises).where(Exercises.difficulty == difficulty)
    )

    exercises = result.scalars().all()

    if not exercises:
        logger.warning(f'No exercises found with difficulty {difficulty}')
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'No exercises found with difficulty {difficulty}',
        )

    logger.info(f'Exercises with difficulty {difficulty}')

    return {'exercises': exercises}


@router.get(
    '/{muscle_group}',
    status_code=HTTPStatus.OK,
    summary=config['get_exercises_muscle_group']['summary'],
    description=config['get_exercises_muscle_group']['description'],
    response_description=config['get_exercises_muscle_group'][
        'resp_description'
    ],
)
async def get_exercises_muscle_group():
    return False



@router.get(
    '/by_equipment_needed/',
    response_model=ExercisePublicList,
    status_code=HTTPStatus.OK,
    summary=config['get_exercises_equipment_needed']['summary'],
    description=config['get_exercises_equipment_needed']['description'],
    response_description=config['get_exercises_equipment_needed'][
        'resp_description'
    ],
)
async def get_exercises_equipment_needed_and(
    session: Session, equipment: List[str] = Query(..., alias='equipment')
 
):
    results = await session.execute(
        select(Exercises).where(
            and_(*[
                Exercises.equipment_needed.contains(eq) for eq in equipment
            ])
        )
    )
    exercises = results.scalars().all()

    if not exercises:
        logger.warning(f'No exercises found with equipment {equipment}')
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'No exercises found with equipment {equipment}',
        )
    logger.info(f'Exercises with equipment {equipment}')

    return {'exercises': exercises}


# ------------------------- POST -------------------------#
@router.post(
    '/',
    response_model=ExercisePublic,
    status_code=HTTPStatus.CREATED,
    summary=config['create_exercise']['summary'],
    description=config['create_exercise']['description'],
    response_description=config['create_exercise']['resp_description'],
)
async def create_exercise(exercice: ExerciseCreate, session: Session):
    result = await session.execute(
        select(Exercises).where(Exercises.name == exercice.name)
    )

    if result.scalars().all():
        logger.warning(f'Exercise {exercice.name} already exists')
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=f'Exercise {exercice.name} already exists',
        )

    new_exercise = Exercises(**exercice.dict())
    session.add(new_exercise)
    await session.commit()
    await session.refresh(new_exercise)
    logger.info(f'Exercise {new_exercise.name} created')

    return new_exercise


# ------------------------- PATCH -------------------------#
@router.patch(
    '/{exercise_id}',
    response_model=ExercisePublic,
    status_code=HTTPStatus.OK,
    summary=config['update_exercise']['summary'],
    description=config['update_exercise']['description'],
    response_description=config['update_exercise']['resp_description'],
)
async def update_exercise(
    exercise_id: int, exercise_update: ExerciseUpdate, session: Session
):
    result = await session.execute(
        select(Exercises).where(Exercises.id == exercise_id)
    )
    existing_exercise = result.scalars().first()

    if not existing_exercise:
        logger.warning(f'Exercise with id {exercise_id} not found')
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Exercise with id {exercise_id} not found',
        )

    # Atualiza apenas os campos passados no payload
    for key, value in exercise_update.dict(exclude_unset=True).items():
        setattr(existing_exercise, key, value)

    await session.commit()
    await session.refresh(existing_exercise)
    logger.info(f'Exercise {existing_exercise.name} updated')

    return existing_exercise


@router.patch(
    '/{exercise_id}/medias',
    response_model=ExercisePublic,
    status_code=HTTPStatus.OK,
    summary=config['update_exercise_midias']['summary'],
    description=config['update_exercise_midias']['description'],
    response_description=config['update_exercise_midias']['resp_description'],
)
async def update_exercise_midias(
    exercise_id: int, exercise_update: ExerciseUpdateMidia, session: Session
):
    result = await session.execute(
        select(Exercises).where(Exercises.id == exercise_id)
    )
    existing_exercise = result.scalars().first()

    if not existing_exercise:
        logger.warning(f'Exercise with id {exercise_id} not found')
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Exercise with id {exercise_id} not found',
        )

    # Atualiza apenas os campos passados no payload
    for key, value in exercise_update.dict(exclude_unset=True).items():
        setattr(existing_exercise, key, value)

    await session.commit()
    await session.refresh(existing_exercise)
    logger.info(f'Exercise {existing_exercise.name} updated')

    return existing_exercise


# ------------------------- DELETE -------------------------#


@router.delete(
    '/{exercise_id}',
    status_code=HTTPStatus.NO_CONTENT,
    summary=config['delete_exercise']['summary'],
    description=config['delete_exercise']['description'],
    response_description=config['delete_exercise']['resp_description'],
)
async def delete_exercise(
    exercise_id: int,
    session: Session,
):
    result = await session.execute(
        select(Exercises).where(Exercises.id == exercise_id)
    )
    existing_exercise = result.scalars().first()

    if not existing_exercise:
        logger.warning(f'Exercise with id {exercise_id} not found')
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Exercise with id {exercise_id} not found',
        )

    await session.delete(existing_exercise)
    await session.commit()
    logger.info(
        f'Exercise {existing_exercise.name} deleted',
        extra={'exercise_id': exercise_id},
    )
