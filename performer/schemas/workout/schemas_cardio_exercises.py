from pydantic import BaseModel


class CardioExerciseCreate(BaseModel):
    name: str
    duration: int
    calories_burned: int


class CardioExercisePublic(BaseModel):
    id: int
    name: str
    duration: int
    calories_burned: int

    class Config:
        from_attributes = True


class CardioExerciseUpdate(BaseModel):
    name: str
    duration: int
    calories_burned: int
