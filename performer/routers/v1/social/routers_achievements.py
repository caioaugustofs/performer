from fastapi import APIRouter

router = APIRouter(
    prefix='/social/achievements',
    tags=['Achievements'],
)


@router.get('/')
async def get_achievements():
    """
    Get all achievements
    """
    return {'message': 'Get all achievements'}


# ------------------------- GET -------------------------#
# ------------------------- POST -------------------------#
# ------------------------- PATCH -------------------------#
# ------------------------- DELETE -------------------------#
