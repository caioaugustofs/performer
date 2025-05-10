from fastapi import APIRouter

router = APIRouter(
    prefix='/workouts/cardio-exercises',
    tags=['Cardio Exercises'],
)


@router.get('/')
async def get_cardio_exercises():
    """
    Get all cardio exercises
    """
    return {'message': 'Get all cardio exercises'}
