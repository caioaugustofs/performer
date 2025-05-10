from pydantic import BaseModel


class SocialLikeCreate(BaseModel):
    post_id: int
    user_id: int


class SocialLikePublic(BaseModel):
    id: int
    post_id: int
    user_id: int

    class Config:
        from_attributes = True
