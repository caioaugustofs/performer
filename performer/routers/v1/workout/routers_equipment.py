from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
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
Session = Annotated[AsyncSession, Depends(get_session)]


# ------------------------- GET -------------------------#
@router.get('/', response_model=EquipmentPublicList, status_code=HTTPStatus.OK)
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
    '/search/muscle_group',
    status_code=HTTPStatus.OK,
)
async def search_equipment_by_muscle_group():
    return False


# ------------------------- POST -------------------------#


@router.post(
    '/', response_model=EquipmentPublic, status_code=HTTPStatus.CREATED
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


@router.delete('/detele/{equipment_id}', status_code=HTTPStatus.NO_CONTENT)
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
