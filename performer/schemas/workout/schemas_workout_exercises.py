from pydantic import BaseModel


class WorkoutExerciseCreate(BaseModel):
    workout_id: int
    exercise_id: int
    repetitions: int


class WorkoutExercisePublic(BaseModel):
    id: int
    workout_id: int
    exercise_id: int
    repetitions: int

    class Config:
        from_attributes = True


class WorkoutExerciseUpdate(BaseModel):
    repetitions: int
