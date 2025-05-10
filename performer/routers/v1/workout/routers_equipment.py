from fastapi import APIRouter

router = APIRouter(
    prefix='/equipment',
    tags=['Equipment'],
)


@router.get('/')
async def get_equipment():
    """
    Get all equipment
    """
    return {'message': 'Get all equipment'}
