from fastapi import APIRouter

router = APIRouter(
    prefix='/social/likes',
    tags=['Social Likes'],
)


@router.get('/')
async def get_social_likes():
    """
    Get all social likes
    """
    return {'message': 'Get all social likes'}


# ------------------------- GET -------------------------#
# ------------------------- POST -------------------------#
# ------------------------- PATCH -------------------------#
# ------------------------- DELETE -------------------------#
