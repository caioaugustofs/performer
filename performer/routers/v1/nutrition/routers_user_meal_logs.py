from fastapi import APIRouter

router = APIRouter(
    prefix='/nutrition/user-meal-logs',
    tags=['User Meal Logs'],
)


@router.get('/')
async def get_user_meal_logs():
    """
    Get all user meal logs
    """
    return {'message': 'Get all user meal logs'}
