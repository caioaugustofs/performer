from fastapi import APIRouter

router = APIRouter(
    prefix='/social/user-achievements',
    tags=['User Achievements'],
)


@router.get('/')
async def get_user_achievements():
    """
    Get all user achievements
    """
    return {'message': 'Get all user achievements'}
