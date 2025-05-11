from fastapi import APIRouter

router = APIRouter(
    prefix='/nutrition/food-items',
    tags=['Food Items'],
)


@router.get('/')
async def get_food_items():
    """
    Get all food items
    """
    return {'message': 'Get all food items'}


# ------------------------- GET -------------------------#
# ------------------------- POST -------------------------#
# ------------------------- PATCH -------------------------#
# ------------------------- DELETE -------------------------#
