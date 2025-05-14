from http import HTTPStatus
from typing import Annotated, List

import toml
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from performer.database import get_session
from performer.model.models import Equipment
from performer.schemas.workout.schemas_equipment import (
    EquipmentCreate,
    EquipmentPublic,
    EquipmentPublicList,
    EquipmentUpdate,
)
from performer.tools.tool_logs import logger

router = APIRouter(
    prefix='/equipment',
    tags=['Equipment'],
)

config = toml.load(r'performer/docs/workout/routers_equipment.toml')

Session = Annotated[AsyncSession, Depends(get_session)]


# ------------------------- GET -------------------------#
@router.get(
    '/',
    response_model=EquipmentPublicList,
    status_code=HTTPStatus.OK,
    summary=config['get_equipment']['summary'],
    description=config['get_equipment']['description'],
    response_description=config['get_equipment']['resp_description'],
)
async def get_equipment(session: Session):
    result = await session.execute(select(Equipment))
    equipment = result.scalars().all()
    if not equipment:
        logger
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='No equipment found',
        )
    logger.info('Equipment list retrieved successfully')
    return {'equipment': equipment}


@router.get(
    '/{equipment_id}',
    response_model=EquipmentPublic,
    status_code=HTTPStatus.OK,
    summary=config['get_equipment_by_id']['summary'],
    description=config['get_equipment_by_id']['description'],
    response_description=config['get_equipment_by_id']['resp_description'],
)
async def get_equipment_by_id(equipment_id: int, session: Session):
    result = await session.execute(
        select(Equipment).where(Equipment.id == equipment_id)
    )
    equipment = result.scalar()
    if not equipment:
        logger.info(f'Equipment with id {equipment_id} not found')
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Equipment with id {equipment_id} not found',
        )
    logger.info(f'Equipment with id {equipment_id} retrieved successfully')
    return equipment


@router.get(
    '/search/muscle_group/',
    status_code=HTTPStatus.OK,
    response_model=EquipmentPublicList,
    summary=config['search_equipment_by_muscle_group']['summary'],
    description=config['search_equipment_by_muscle_group']['description'],
    response_description=config['search_equipment_by_muscle_group'][
        'resp_description'
    ],
)
async def search_equipment_by_muscle_group(
    session: Session, muscle: List[str] = Query(..., alias='muscle_group')
):
    result = await session.execute(
        select(Equipment).where(
            and_(*[Equipment.muscle_group.contains(mg) for mg in muscle])
        )
    )

    exercises = result.scalars().all()

    if not exercises:
        logger.warning(f'No equipment found with muscle group {muscle}')
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'No equipment found with muscle group {muscle}',
        )
    logger.info(f'Equipment with muscle group {muscle} retrieved successfully')
    return {'equipment': exercises}


# ------------------------- POST -------------------------#


@router.post(
    '/',
    response_model=EquipmentPublic,
    status_code=HTTPStatus.CREATED,
    summary=config['create_equipment']['summary'],
    description=config['create_equipment']['description'],
    response_description=config['create_equipment']['resp_description'],
)
async def create_equipment(equipment: EquipmentCreate, session: Session):
    result = await session.execute(
        select(Equipment).where(Equipment.name == equipment.name)
    )
    existing_equipment = result.scalars().all()

    if existing_equipment:
        logger.info(f'Equipment with name {equipment.name} already exists')
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=f'Equipment with name {equipment.name} already exists',
        )

    new_equipment = Equipment(**equipment.model_dump())

    session.add(new_equipment)

    await session.commit()
    await session.refresh(new_equipment)

    logger.info(f'Equipment created successfully with id {new_equipment.id}')
    return new_equipment


# busta em uma lista do grupo muscular


# ------------------------- PATCH -------------------------#


@router.patch(
    '/{equipment_id}',
    response_model=EquipmentPublic,
    status_code=HTTPStatus.OK,
    summary=config['update_equipment']['summary'],
    description=config['update_equipment']['description'],
    response_description=config['update_equipment']['resp_description'],
)
async def update_equipment(
    equipment_id: int, equipment: EquipmentUpdate, session: Session
):
    result = await session.execute(
        select(Equipment).where(Equipment.id == equipment_id)
    )
    existing_equipment = result.scalar()
    if not existing_equipment:
        logger.info(f'Equipment with id {equipment_id} not found')
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Equipment with id {equipment_id} not found',
        )

    for key, value in equipment.model_dump().items():
        if value is not None:  # Only update fields with non-None values
            setattr(existing_equipment, key, value)

    await session.commit()
    await session.refresh(existing_equipment)
    logger.info(f'Equipment with id {equipment_id} updated successfully')
    return existing_equipment


# ------------------------- DELETE -------------------------#


@router.delete(
    '/detele/{equipment_id}',
    status_code=HTTPStatus.NO_CONTENT,
    summary=config['delete_equipment']['summary'],
    description=config['delete_equipment']['description'],
    response_description=config['delete_equipment']['resp_description'],
)
async def delete_equipment(equipment_id: int, session: Session):
    result = await session.execute(
        select(Equipment).where(Equipment.id == equipment_id)
    )
    existing_equipment = result.scalar()
    if not existing_equipment:
        logger.info(f'Equipment with id {equipment_id} not found')
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Equipment with id {equipment_id} not found',
        )

    await session.delete(existing_equipment)
    await session.commit()
    logger.info(f'Equipment with id {equipment_id} deleted successfully')
