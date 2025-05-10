from fastapi import APIRouter

router = APIRouter(
    prefix='/workouts/user-cardio-logs',
    tags=['User Cardio Logs'],
)


@router.get('/')
async def get_user_cardio_logs():
    """
    Get all user cardio logs
    """
    return {'message': 'Get all user cardio logs'}
