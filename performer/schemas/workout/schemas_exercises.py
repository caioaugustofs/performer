from typing import List, Optional

from pydantic import BaseModel


class ExerciseCreate(BaseModel):
    name: str
    description: Optional[str] = None
    difficulty: int
    muscle_group: Optional[list[str]] = None
    equipment_needed: Optional[list[str]] = None
    tags: Optional[list[str]] = None
    calories_burned_estimated: Optional[float] = None
    video_url: Optional[str] = None
    image_url: Optional[str] = None


class ExercisePublic(BaseModel):
    id: int
    name: str
    difficulty: int
    muscle_group: list[str] | None = None
    equipment_needed: list[str] | None = None
    tags: list[str] | None = None
    calories_burned_estimated: Optional[float] = None
    video_url: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class ExercisePublicList(BaseModel):
    exercises: List[ExercisePublic]


class ExerciseUpdate(BaseModel):
    name: Optional[str] | None = None
    description: Optional[str] | None = None
    difficulty: Optional[int] | None = None
    muscle_group: Optional[list[str]] | None = None
    equipment_needed: Optional[list[str]] | None = None
    tags: Optional[list[str]] | None = None
    calories_burned_estimated: Optional[float] | None = None


class ExerciseUpdateMidia(BaseModel):
    video_url: Optional[str] | None = None
    image_url: Optional[str] | None = None
