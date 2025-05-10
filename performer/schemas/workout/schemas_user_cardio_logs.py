from pydantic import BaseModel


class UserCardioLogCreate(BaseModel):
    user_id: int
    duration: int
    calories_burned: int


class UserCardioLogPublic(BaseModel):
    id: int
    user_id: int
    duration: int
    calories_burned: int

    class Config:
        from_attributes = True


class UserCardioLogUpdate(BaseModel):
    duration: int
    calories_burned: int
