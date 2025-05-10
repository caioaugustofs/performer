from pydantic import BaseModel


class SocialPostCreate(BaseModel):
    content: str
    user_id: int


class SocialPostPublic(BaseModel):
    id: int
    content: str
    user_id: int

    class Config:
        from_attributes = True


class SocialPostUpdate(BaseModel):
    content: str
