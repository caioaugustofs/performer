from fastapi import APIRouter

router = APIRouter(
    prefix='/workouts/user-hiit-logs',
    tags=['User HIIT Logs'],
)


@router.get('/')
async def get_user_hiit_logs():
    """
    Get all user HIIT logs
    """
    return {'message': 'Get all user HIIT logs'}
