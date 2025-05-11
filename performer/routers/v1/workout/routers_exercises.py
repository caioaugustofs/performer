from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
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

router = APIRouter(prefix='/exercises', tags=['Exercises'])

Session = Annotated[AsyncSession, Depends(get_session)]


# ------------------------- GET -------------------------#
@router.get('/', response_model=ExercisePublicList, status_code=HTTPStatus.OK)
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
)
async def get_exercises_difficulty(difficulty: int, session: Session):
    result = await session.execute(
        select(Exercises).where(Exercises.difficulty == difficulty)
    )

    exercises = result.scalars().all()
    logger.info(f'Exercises with difficulty {difficulty}')

    return {'exercises': exercises}


@router.get(
    '/{muscle_group}',
    response_model=ExercisePublicList,
    status_code=HTTPStatus.OK,
)
async def get_exercises_muscle_group(muscle_group: str, session: Session):
    result = await session.execute(
        select(Exercises).where(Exercises.muscle_group == muscle_group)
    )
    exercises = result.scalars().all()
    logger.info(f'Exercises with muscle group {muscle_group}')

    return {'exercises': exercises}


@router.get(
    '/{equipment_needed}',
    response_model=ExercisePublicList,
    status_code=HTTPStatus.OK,
)
async def get_exercises_equipment_needed(
    equipment_needed: str, session: Session
):
    result = await session.execute(
        select(Exercises).where(Exercises.equipment_needed == equipment_needed)
    )
    exercises = result.scalars().all()
    logger.info(f'Exercises with equipment needed {equipment_needed}')

    return {'exercises': exercises}


# ------------------------- POST -------------------------#
@router.post(
    '/',
    response_model=ExercisePublic,
    status_code=HTTPStatus.CREATED,
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
        return None

    await session.delete(existing_exercise)
    await session.commit()
    logger.info(f'Exercise {existing_exercise.name} deleted')
