from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from performer.database import get_session
from performer.models import User
from performer.schemas.schemas_users import (UserCreateSchema, UserEmailUpdate,
                                             UserList, UserPassworrdUpdate,
                                             UserPublicSchema,
                                             UserUsernameUpdate)

router = APIRouter(prefix="/users", tags=["Users"])

Session_ = Annotated[Session, Depends(get_session)]


@router.post(
    "/", status_code=HTTPStatus.CREATED, response_model=UserPublicSchema
)
def create_user(user: UserCreateSchema, session: Session_):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Username or Email already exists",
        )

    db_user = User(
        username=user.username, password=user.password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get("/", status_code=HTTPStatus.OK, response_model=UserList)
def get_users(session: Session_, skip: int = 0, limit: int = 100):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {"users": users}


@router.get(
    "/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublicSchema
)
def get_user(user_id: int):
    return {"user_id": user_id}


@router.patch("/password/user_id}", status_code=HTTPStatus.OK)
def update_password(user_id: int, user: UserPassworrdUpdate):
    return True


@router.patch("/username/user_id}", status_code=HTTPStatus.OK)
def update_username(user_id: int, user: UserUsernameUpdate, session: Session_):
    return True


@router.patch("/email/user_id}", status_code=HTTPStatus.OK)
def update_email(user_id: int, user: UserEmailUpdate, session: Session_):
    return True


@router.delete("/{user_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int, session: Session_):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )

    session.delete(db_user)
    session.commit()

    return {"message": "User deleted"}
