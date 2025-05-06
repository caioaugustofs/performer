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
        orm_mode = True


class UserList(BaseModel):
    users: list[UserPublicSchema]
