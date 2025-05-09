from pydantic import BaseModel


class UserWorkoutSessionAdd(BaseModel):
    user_id: int


class UserWorkoutSessionPublic(BaseModel):
    user_id: int
    workout_session_id: int
