from datetime import datetime

from sqlalchemy import JSON, func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    email_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    password_reset_token: Mapped[str] = mapped_column(
        unique=True, default='', nullable=True
    )
    last_login: Mapped[datetime] = mapped_column(default=None, nullable=True)
    role: Mapped[str] = mapped_column(default='user', nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    subscription_status: Mapped[str] = mapped_column(
        default='free', nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )


@table_registry.mapped_as_dataclass
class User_details:
    __tablename__ = 'user_details'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(init=False)
    data_de_nascimento: Mapped[str] = mapped_column(
        default=None, nullable=True
    )
    altura: Mapped[float] = mapped_column(default=None, nullable=True)
    peso: Mapped[float] = mapped_column(default=None, nullable=True)
    sexo: Mapped[str] = mapped_column(default=None, nullable=True)
    objetivo: Mapped[str] = mapped_column(default=None, nullable=True)
    fitness_level: Mapped[str] = mapped_column(default=None, nullable=True)
    equipment_available: Mapped[list] = mapped_column(
        JSON, default=None, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
