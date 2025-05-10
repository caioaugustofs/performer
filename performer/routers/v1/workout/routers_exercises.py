from fastapi import APIRouter

router = APIRouter(
    prefix='/workouts/exercises',
    tags=['Exercises'],
)


@router.get('/')
async def get_exercises():
    """
    Get all exercises
    """
    return {'message': 'Get all exercises'}
