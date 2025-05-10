from pydantic import BaseModel


class EquipmentCreate(BaseModel):
    name: str
    type: str


class EquipmentPublic(BaseModel):
    id: int
    name: str
    type: str

    class Config:
        from_attributes = True


class EquipmentUpdate(BaseModel):
    name: str
    type: str
