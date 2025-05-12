from typing import Optional

from pydantic import BaseModel


class EquipmentCreate(BaseModel):
    name: str
    description: str | None = None
    image_url: str | None = None
    muscle_group: list[str] | None = None
    tags: list[str] | None = None


class EquipmentPublic(BaseModel):
    id: int
    name: str
    description: str | None = None
    image_url: str | None = None
    muscle_group: list[str] | None = None
    tags: list[str] | None = None

    class Config:
        from_attributes = True


class EquipmentPublicList(BaseModel):
    equipment: list[EquipmentPublic]

    class Config:
        from_attributes = True


class EquipmentUpdate(BaseModel):
    name: Optional[str] | None = None
    description: Optional[str] | None = None
    image_url: Optional[str] | None = None
    muscle_group: Optional[list[str]] | None = None
    tags: Optional[list[str]] | None = None
