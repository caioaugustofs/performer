from fastapi import APIRouter

router = APIRouter(
    prefix='/workouts/workout-exercises',
    tags=['Workout Exercises'],
)


@router.get('/')
async def get_workout_exercises():
    """
    Get all workout exercises
    """
    return {'message': 'Get all workout exercises'}
