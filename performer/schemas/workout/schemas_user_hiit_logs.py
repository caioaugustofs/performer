from pydantic import BaseModel


class UserHIITLogCreate(BaseModel):
    user_id: int
    duration: int
    calories_burned: int


class UserHIITLogPublic(BaseModel):
    id: int
    user_id: int
    duration: int
    calories_burned: int

    class Config:
        from_attributes = True


class UserHIITLogUpdate(BaseModel):
    duration: int
    calories_burned: int
