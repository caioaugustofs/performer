from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from .models import table_registry


@table_registry.mapped_as_dataclass
class Achievements:
    __tablename__ = 'achievements'
    id: Mapped[int] = mapped_column(init=False, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    icon_url: Mapped[str] = mapped_column(nullable=False)


@table_registry.mapped_as_dataclass
class UserAchievements:
    __tablename__ = 'user_achievements'
    id: Mapped[int] = mapped_column(init=False, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    achievement_id: Mapped[int] = mapped_column(nullable=False)
    unlocked_at: Mapped[datetime] = mapped_column(
        default=func.now(), nullable=False
    )


@table_registry.mapped_as_dataclass
class SocialPosts:
    __tablename__ = 'social_posts'
    id: Mapped[int] = mapped_column(init=False, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    media_url: Mapped[str | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), nullable=False
    )


@table_registry.mapped_as_dataclass
class SocialComments:
    __tablename__ = 'social_comments'
    id: Mapped[int] = mapped_column(init=False, primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), nullable=False
    )


@table_registry.mapped_as_dataclass
class SocialLikes:
    __tablename__ = 'social_likes'
    id: Mapped[int] = mapped_column(init=False, primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), nullable=False
    )
