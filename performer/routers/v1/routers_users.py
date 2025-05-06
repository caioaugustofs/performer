from http import HTTPStatus

from fastapi import APIRouter

from performer.schemas.schemas_users import (
    UserCreateSchema,
    UserList,
    UserPublicSchema,
)

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=UserPublicSchema
)
def create_user(user: UserCreateSchema):
    """
    Create a new user.
    """
    return True


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def get_users():
    return {'users': []}


@router.patch('/users/{user_id}', status_code=HTTPStatus.OK)
def update_user(user_id: int, user: UserCreateSchema):
    return True


@router.delete('/users/{user_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int):
    return None
