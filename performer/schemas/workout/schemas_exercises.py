from pydantic import BaseModel


class ExerciseCreate(BaseModel):
    name: str
    difficulty: int


class ExercisePublic(BaseModel):
    id: int
    name: str
    difficulty: int

    class Config:
        from_attributes = True


class ExerciseUpdate(BaseModel):
    name: str
    difficulty: int
