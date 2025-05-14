from pydantic import BaseModel


class WorkoutPublic(BaseModel):
    id: int
    name: str
    duration_min: int
    difficulty: int
    type: str


class WorkoutPublicList(BaseModel):
    workouts: list[WorkoutPublic]


class WorkoutCreate(BaseModel):
    name: str
    duration_min: int = 1
    is_public: bool = False
    difficulty: int = 1
    type: str | None = None
    rest_between_exercises_seconds: int | None = None


class WorkoutFull(BaseModel):
    id: int
    created_by: int
    name: str
    duration_min: int
    is_public: bool
    difficulty: int
    type: str
    rest_between_exercises_seconds: int | None = None


class WorkoutUpdate(BaseModel):
    name: str
    duration_min: int
    is_public: bool = True
    difficulty: int = 1
    type: str
    rest_between_exercises_seconds: int | None = None


class WorkoutFullList(BaseModel):
    workouts: list[WorkoutFull]
