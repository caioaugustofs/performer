from http import HTTPStatus

from fastapi import APIRouter

from performer.schemas.schemas_users import (
    UserCreateSchema,
    UserEmailUpdate,
    UserList,
    UserPassworrdUpdate,
    UserPublicSchema,
    UserUsernameUpdate,
)

router = APIRouter(prefix='/users', tags=['Users'])


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


@router.get(
    '/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublicSchema
)
def get_user(user_id: int):
    return {'user_id': user_id}


@router.patch('/password/user_id}', status_code=HTTPStatus.OK)
def update_password(user_id: int, user: UserPassworrdUpdate):
    return True


@router.patch('/email/user_id}', status_code=HTTPStatus.OK)
def update_email(user_id: int, user: UserEmailUpdate):
    return True


@router.patch('/username/user_id}', status_code=HTTPStatus.OK)
def update_username(user_id: int, user: UserUsernameUpdate):
    return True


@router.delete('/{user_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int):
    return None
