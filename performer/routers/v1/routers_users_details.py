from fastapi import APIRouter

router = APIRouter(prefix='/detail', tags=['Users', 'detail'])


@router.get('/')
def get_info_user(): ...


@router.get('/{user_id}')
def get_info_user_by_id(): ...


@router.post('/add')
def add_info_user(): ...
