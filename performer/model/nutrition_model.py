from datetime import datetime

from sqlalchemy import JSON, func
from sqlalchemy.orm import Mapped, mapped_column

from .models import table_registry


@table_registry.mapped_as_dataclass
class Food_Items:
    __tablename__ = 'food_items'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    tags: Mapped[list] = mapped_column(JSON, nullable=True)
    calories_per_100g: Mapped[float] = mapped_column(nullable=False)
    protein: Mapped[float] = mapped_column(nullable=False)
    carbs: Mapped[float] = mapped_column(nullable=False)
    fats: Mapped[float] = mapped_column(nullable=False)
    fiber: Mapped[float] = mapped_column(nullable=False)
    sugar: Mapped[float] = mapped_column(nullable=False)
    sodium: Mapped[float] = mapped_column(nullable=False)
    is_vegan: Mapped[bool] = mapped_column(nullable=False)
    is_vegetarian: Mapped[bool] = mapped_column(nullable=False)
    is_gluten_free: Mapped[bool] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )


@table_registry.mapped_as_dataclass
class User_Meal_Logs:
    __tablename__ = 'user_meal_logs'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    custom_food_name: Mapped[str] = mapped_column(nullable=True)
    custom_food_description: Mapped[str] = mapped_column(nullable=True)
    meal_calories: Mapped[float] = mapped_column(nullable=False)
    quantity_grams: Mapped[float] = mapped_column(nullable=False)
    food_item_id: Mapped[int] = mapped_column(nullable=False)
    meal_time: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(nullable=False)
