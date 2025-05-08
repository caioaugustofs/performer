from datetime import datetime
from sqlalchemy import JSON, func
from sqlalchemy.orm import Mapped, mapped_column
from .models import table_registry

@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    email_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    password_reset_token: Mapped[str] = mapped_column(unique=True, default='', nullable=True)
    last_login: Mapped[datetime] = mapped_column(default=None, nullable=True)
    role: Mapped[str] = mapped_column(default='user', nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    subscription_status: Mapped[str] = mapped_column(default='free', nullable=False)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

@table_registry.mapped_as_dataclass
class User_details:
    __tablename__ = 'user_details'
    id: Mapped[int] = mapped_column(init=False, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(nullable=False, index=True)
    data_de_nascimento: Mapped[str] = mapped_column(default=None, nullable=True)
    altura: Mapped[float] = mapped_column(default=None, nullable=True)
    peso: Mapped[float] = mapped_column(default=None, nullable=True)
    sexo: Mapped[str] = mapped_column(default=None, nullable=True)
    objetivo: Mapped[str] = mapped_column(default=None, nullable=True)
    fitness_level: Mapped[str] = mapped_column(default=None, nullable=True)
    goal: Mapped[list] = mapped_column(JSON, default=None, nullable=True)
    profile_picture_url: Mapped[str] = mapped_column(default=None, nullable=True)
    preferred_units: Mapped[str] = mapped_column(default='metric', nullable=False)
    equipment_available: Mapped[list] = mapped_column(JSON, default=None, nullable=True)
    injuries: Mapped[list] = mapped_column(JSON, default=None, nullable=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

@table_registry.mapped_as_dataclass
class User_Workout_Sessions:
    __tablename__ = 'user_workout_sessions'
    id: Mapped[int] = mapped_column(init=False, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(nullable=False, index=True)
    workout_id: Mapped[int] = mapped_column(nullable=False, index=True)
    start_time: Mapped[datetime] = mapped_column(default=None, nullable=True)
    end_time: Mapped[datetime] = mapped_column(default=None, nullable=True)
    calories_burned: Mapped[float] = mapped_column(default=None, nullable=True)
    difficulty_perceived: Mapped[int] = mapped_column(default=None, nullable=True)
    rating: Mapped[int] = mapped_column(default=None, nullable=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

@table_registry.mapped_as_dataclass
class User_Workout_Schedules:
    __tablename__ = 'user_workout_schedules'
    id: Mapped[int] = mapped_column(init=False, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(nullable=False, index=True)
    workout_id: Mapped[int] = mapped_column(nullable=False, index=True)
    scheduled_date: Mapped[datetime] = mapped_column(default=None, nullable=True)
    scheduled_time: Mapped[datetime] = mapped_column(default=None, nullable=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

@table_registry.mapped_as_dataclass
class User_Exercise_Logs:
    __tablename__ = 'user_exercise_logs'
    id: Mapped[int] = mapped_column(init=False, primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(nullable=False, index=True)
    exercise_id: Mapped[int] = mapped_column(nullable=False, index=True)
    weight_used: Mapped[str] = mapped_column(default=None, nullable=True)
    reps_completed: Mapped[int] = mapped_column(default=None, nullable=True)
    review: Mapped[int] = mapped_column(default=None, nullable=True)
    notes_info: Mapped[str] = mapped_column(default=None, nullable=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

@table_registry.mapped_as_dataclass
class Progress_Tracking:
    __tablename__ = 'progress_tracking'
    id: Mapped[int] = mapped_column(init=False, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(nullable=False, index=True)
    peso: Mapped[float] = mapped_column(default=None, nullable=True)
    altura: Mapped[float] = mapped_column(default=None, nullable=True)
    body_measurements: Mapped[dict] = mapped_column(JSON, default=None, nullable=True)
    date: Mapped[datetime] = mapped_column(default=None, nullable=True)