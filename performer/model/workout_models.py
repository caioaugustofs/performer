from datetime import datetime

from sqlalchemy import JSON, Column, ForeignKey, Integer, Table, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .models import table_registry


@table_registry.mapped_as_dataclass
class Workouts:
    __tablename__ = 'workouts'
    id: Mapped[int] = mapped_column(init=False, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(default=None, nullable=True)
    duration_min: Mapped[int] = mapped_column(default=None, nullable=True)
    difficulty: Mapped[int] = mapped_column(default=None, nullable=True)
    type: Mapped[str] = mapped_column(default=None, nullable=True)
    rest_between_exercises_seconds: Mapped[int] = mapped_column(
        default=None, nullable=True
    )
    is_public: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_by: Mapped[int] = mapped_column(default=None, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    exercises = relationship('Workout_Exercises', back_populates='workout')


@table_registry.mapped_as_dataclass
class Exercises:
    __tablename__ = 'exercises'
    id: Mapped[int] = mapped_column(init=False, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(default=None, nullable=True)
    description: Mapped[str] = mapped_column(default=None, nullable=True)
    video_url: Mapped[str] = mapped_column(default=None, nullable=True)
    image_url: Mapped[str] = mapped_column(default=None, nullable=True)
    muscle_group: Mapped[list] = mapped_column(
        JSON, default=None, nullable=True
    )
    equipment_needed: Mapped[list] = mapped_column(
        JSON, default=None, nullable=True
    )
    difficulty: Mapped[int] = mapped_column(default=None, nullable=True)
    tags: Mapped[list] = mapped_column(JSON, default=None, nullable=True)
    calories_burned_estimated: Mapped[float] = mapped_column(
        default=None, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    workout_exercises = relationship(
        'Workout_Exercises', back_populates='exercise'
    )
    equipment = relationship(
        'Equipment', secondary='exercise_equipment', back_populates='exercises'
    )


@table_registry.mapped_as_dataclass
class Workout_Exercises:
    __tablename__ = 'workout_exercises'
    id: Mapped[int] = mapped_column(init=False, primary_key=True, index=True)
    workout_id: Mapped[int] = mapped_column(
        ForeignKey('workouts.id', name='fk_workout_exercises_workout_id'),
        nullable=False,
        index=True,
    )
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey('exercises.id', name='fk_workout_exercises_exercise_id'),
        nullable=False,
        index=True,
    )
    exercise_type: Mapped[str] = mapped_column(nullable=False)
    cardio_exercise_id: Mapped[int | None] = mapped_column(nullable=True)
    target_duration_minutes: Mapped[int | None] = mapped_column(nullable=True)
    target_distance_km: Mapped[float | None] = mapped_column(nullable=True)
    target_speed_kmh: Mapped[float | None] = mapped_column(nullable=True)
    sets: Mapped[int] = mapped_column(default=None, nullable=True)
    reps: Mapped[int] = mapped_column(default=None, nullable=True)
    time_per_rep_seconds: Mapped[int] = mapped_column(
        default=None, nullable=True
    )
    rest_between_sets_seconds: Mapped[int] = mapped_column(
        default=None, nullable=True
    )
    max_rest_between_reps_seconds: Mapped[int] = mapped_column(
        default=None, nullable=True
    )
    rest_seconds: Mapped[int] = mapped_column(default=None, nullable=True)
    order: Mapped[int] = mapped_column(default=None, nullable=True)
    is_warmup: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_cooldown: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    workout = relationship('Workouts', back_populates='exercises')
    exercise = relationship('Exercises', back_populates='workout_exercises')


@table_registry.mapped_as_dataclass
class Equipment:
    __tablename__ = 'equipment'
    id: Mapped[int] = mapped_column(init=False, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    image_url: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    tags: Mapped[list] = mapped_column(JSON, nullable=True)
    muscle_group: Mapped[list] = mapped_column(
        JSON, default=None, nullable=True
    )
    exercises = relationship(
        'Exercises', secondary='exercise_equipment', back_populates='equipment'
    )


@table_registry.mapped_as_dataclass
class UserHIITLogs:
    __tablename__ = 'user_hiit_logs'
    id: Mapped[int] = mapped_column(init=False, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    workout_exercise_id: Mapped[int] = mapped_column(
        ForeignKey(
            'workout_exercises.id',
            name='fk_user_hiit_logs_workout_exercise_id',
        ),
        nullable=False,
    )
    session_id: Mapped[int] = mapped_column(nullable=False)
    set_number: Mapped[int] = mapped_column(nullable=False)
    actual_time_per_rep_seconds: Mapped[float] = mapped_column(nullable=True)
    rest_taken_seconds: Mapped[float] = mapped_column(nullable=True)
    completed_at: Mapped[datetime] = mapped_column(
        default=func.now(), nullable=False
    )
    workout_exercise = relationship('Workout_Exercises')


@table_registry.mapped_as_dataclass
class CardioExercises:
    __tablename__ = 'cardio_exercises'
    id: Mapped[int] = mapped_column(init=False, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    default_duration_minutes: Mapped[int] = mapped_column(nullable=True)
    default_distance_km: Mapped[float] = mapped_column(nullable=True)
    default_calories_burned: Mapped[float] = mapped_column(nullable=True)


@table_registry.mapped_as_dataclass
class UserCardioLogs:
    __tablename__ = 'user_cardio_logs'
    id: Mapped[int] = mapped_column(init=False, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    cardio_exercise_id: Mapped[int] = mapped_column(
        ForeignKey(
            'cardio_exercises.id',
            name='fk_user_cardio_logs_cardio_exercise_id',
        ),
        nullable=False,
    )
    session_id: Mapped[int] = mapped_column(nullable=False)
    duration_minutes: Mapped[int] = mapped_column(nullable=True)
    distance_km: Mapped[float] = mapped_column(nullable=True)
    avg_speed_kmh: Mapped[float] = mapped_column(nullable=True)
    max_speed_kmh: Mapped[float] = mapped_column(nullable=True)
    calories_burned: Mapped[float] = mapped_column(nullable=True)
    incline_percent: Mapped[float] = mapped_column(nullable=True)
    resistance_level: Mapped[int] = mapped_column(nullable=True)
    notes: Mapped[str] = mapped_column(nullable=True)
    cardio_exercise = relationship('CardioExercises')


# Tabela associativa para o relacionamento muitos-para-muitos
exercise_equipment = Table(
    'exercise_equipment',
    table_registry.metadata,
    Column(
        'exercise_id',
        ForeignKey('exercises.id'),
        primary_key=True,
        type_=Integer,
    ),
    Column(
        'equipment_id',
        ForeignKey('equipment.id'),
        primary_key=True,
        type_=Integer,
    ),
)
