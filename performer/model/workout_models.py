from datetime import datetime
from sqlalchemy import JSON, func
from sqlalchemy.orm import Mapped, mapped_column
from .models import table_registry

@table_registry.mapped_as_dataclass
class Workouts:
    __tablename__ = 'workouts'
    id: Mapped[int] = mapped_column(init=False, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(default=None, nullable=True)
    duration_min: Mapped[int] = mapped_column(default=None, nullable=True)
    difficulty: Mapped[int] = mapped_column(default=None, nullable=True)
    type: Mapped[str] = mapped_column(default=None, nullable=True)
    rest_between_exercises_seconds: Mapped[int] = mapped_column(default=None, nullable=True)
    is_public: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_by: Mapped[int] = mapped_column(default=None, nullable=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

@table_registry.mapped_as_dataclass
class Exercises:
    __tablename__ = 'exercises'
    id: Mapped[int] = mapped_column(init=False, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(default=None, nullable=True)
    description: Mapped[str] = mapped_column(default=None, nullable=True)
    video_url: Mapped[str] = mapped_column(default=None, nullable=True)
    image_url: Mapped[str] = mapped_column(default=None, nullable=True)
    muscle_group: Mapped[list] = mapped_column(JSON, default=None, nullable=True)
    equipment_needed: Mapped[list] = mapped_column(JSON, default=None, nullable=True)
    difficulty: Mapped[int] = mapped_column(default=None, nullable=True)
    tags: Mapped[list] = mapped_column(JSON, default=None, nullable=True)
    calories_burned_estimated: Mapped[float] = mapped_column(default=None, nullable=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

@table_registry.mapped_as_dataclass
class workout_exercises:
    __tablename__ = 'workout_exercises'
    workout_id: Mapped[int] = mapped_column(init=False, primary_key=True, index=True)
    exercise_id: Mapped[int] = mapped_column(init=False, primary_key=True, index=True)
    sets: Mapped[int] = mapped_column(default=None, nullable=True)
    reps: Mapped[int] = mapped_column(default=None, nullable=True)
    rest_seconds: Mapped[int] = mapped_column(default=None, nullable=True)
    order: Mapped[int] = mapped_column(default=None, nullable=True)
    is_warmup: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_cooldown: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())