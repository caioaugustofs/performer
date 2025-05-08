from pydantic import BaseModel


class UserDetailsAdd(BaseModel):
    id: int


class UserDetailsPublic(BaseModel):
    id: int
    user_id: int


class UserDetailsFull(BaseModel):
    id: int
    user_id: int
    data_de_nascimento: str
    altura: float | None = None
    peso: float | None = None


class DetailsList(BaseModel):
    details: list[UserDetailsPublic]
