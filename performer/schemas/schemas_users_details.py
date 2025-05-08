from pydantic import BaseModel


class UserDetailsAdd(BaseModel):
    id: int


class UserDetailsPublic(BaseModel):
    id: int
    user_id: int


class DetailsList(BaseModel):
    details: list[UserDetailsPublic]


class UserDetailsUpdate(BaseModel):
    user_id: int
    data_de_nascimento: str | None = None
    altura: float | None = None
    peso: float | None = None
    sexo: str | None = None
    objetivo: str | None = None
    fitness_level: str | None = None
    equipment_available: list | None = None


class UserDetailsFull(UserDetailsUpdate):
    id: int
