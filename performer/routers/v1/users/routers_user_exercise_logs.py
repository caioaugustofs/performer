from fastapi import APIRouter

router = APIRouter(
    prefix='/user/exercise-logs',
    tags=['User Exercise Logs'],
)


@router.get('/')
async def get_user_exercise_logs():
    """
    Get all user exercise logs
    """
    return {'message': 'Get all user exercise logs'}
