from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    username: str
    email: str
    password: str


class UserPublicSchema(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class UserUsernameUpdate(BaseModel):
    new_username: str


class UserPasswordUpdate(BaseModel):
    email: str
    password: str
    new_password: str


class UserList(BaseModel):
    users: list[UserPublicSchema]
