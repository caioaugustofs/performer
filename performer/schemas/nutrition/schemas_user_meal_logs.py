from pydantic import BaseModel


class UserMealLogCreate(BaseModel):
    user_id: int
    meal_name: str
    calories: int


class UserMealLogPublic(BaseModel):
    id: int
    user_id: int
    meal_name: str
    calories: int

    class Config:
        from_attributes = True


class UserMealLogUpdate(BaseModel):
    meal_name: str
    calories: int
