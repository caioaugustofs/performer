from fastapi import APIRouter

router = APIRouter(
    prefix='/social/posts',
    tags=['Social Posts'],
)


@router.get('/')
async def get_social_posts():
    """
    Get all social posts
    """
    return {'message': 'Get all social posts'}
