from fastapi import APIRouter

router = APIRouter(
    prefix='/social/comments',
    tags=['Social Comments'],
)


@router.get('/')
async def get_social_comments():
    """
    Get all social comments
    """
    return {'message': 'Get all social comments'}


# ------------------------- GET -------------------------#
# ------------------------- POST -------------------------#
# ------------------------- PATCH -------------------------#
# ------------------------- DELETE -------------------------#
