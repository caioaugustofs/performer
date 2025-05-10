from pydantic import BaseModel


class FoodItemCreate(BaseModel):
    name: str
    calories: int


class FoodItemPublic(BaseModel):
    id: int
    name: str
    calories: int

    class Config:
        from_attributes = True


class FoodItemUpdate(BaseModel):
    name: str
    calories: int
