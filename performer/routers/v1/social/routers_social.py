from fastapi import APIRouter

router = APIRouter(
    prefix='/social',
    tags=['Social'],
)


@router.get('/achievements')
async def get_achievements():
    """
    Get all achievements
    """
    return {'message': 'Get all achievements'}


@router.get('/user-achievements')
async def get_user_achievements():
    """
    Get all user achievements
    """
    return {'message': 'Get all user achievements'}


@router.get('/posts')
async def get_social_posts():
    """
    Get all social posts
    """
    return {'message': 'Get all social posts'}


@router.get('/comments')
async def get_social_comments():
    """
    Get all social comments
    """
    return {'message': 'Get all social comments'}


@router.get('/likes')
async def get_social_likes():
    """
    Get all social likes
    """
    return {'message': 'Get all social likes'}
