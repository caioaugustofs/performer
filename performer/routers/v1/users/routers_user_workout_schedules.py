from fastapi import APIRouter

router = APIRouter(
    prefix='/user/workout-schedules',
    tags=['User Workout Schedules'],
)


@router.get('/')
async def get_user_workout_schedules():
    """
    Get all user workout schedules
    """
    return {'message': 'Get all user workout schedules'}
