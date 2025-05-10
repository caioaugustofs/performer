from fastapi import APIRouter

router = APIRouter(
    prefix='/user/progress-tracking',
    tags=['Progress Tracking'],
)


@router.get('/')
async def get_progress_tracking():
    """
    Get all progress tracking data
    """
    return {'message': 'Get all progress tracking data'}
