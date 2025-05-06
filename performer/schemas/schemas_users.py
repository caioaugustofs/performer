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

class UserEmailUpdate(BaseModel):
    email: str

class UserUsernameUpdate(BaseModel):
    username: str

class UserPassworrdUpdate(BaseModel):
    password: str

class UserList(BaseModel):
    users: list[UserPublicSchema]
